import random

from flask import request, make_response, render_template, flash, redirect, url_for, session
from app.main.forms import SimpleFrom
from ..decorators import admin_required, permission_required
from app.models import *
from flask_mail import Message
from .. import mail
from . import main, errors
from app import db, admin
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Basket, db.session))
admin.add_view(ModelView(Category, db.session))


@main.route("/check")
def cookie():
    """
    Function for checking user's browser
    :return: if it is mozilla - set cookie random number in flag
    """
    user_agent = request.headers.get('User-Agent')
    if user_agent.lower().__contains__("mozilla"):
        response = make_response("<H1>Everything is good!<H1>")
        response.set_cookie('flag', str(random.randint(1, 100)))
        return response
    else:
        return "<H1>Everything is bad!<H1>"


@main.route("/index/<name>/<city>")
def town(name, city):
    """
    Function for base input
    :param name: user's name
    :param city: user's city
    :return: Hello user's name. You are from user's town.
    """
    return "<h1>Hello, {}. You are from {}!<h1>".format(name, city)


@main.route("/error")
def error():
    """
    Function for testing error page
    :return: error page
    """
    return errors.page_not_found(error)


@main.route('/')
@main.route('/index')
def index():
    """
    Function for main page
    :return: index template with all items
    """
    items = db.session.query(Item, Category).filter(Item.cat_id == Category.id).all()
    categories = Category.query.all()
    return render_template("index.html", auth=session.get('auth'), items=items, categories=categories)


@main.route("/items/<item_id>", methods=['GET', 'POST'])
def show_item(item_id):
    """
    Function for showing one item and adding to the basket
    :param item_id: number of item
    :return: if item doesn't exist - return 404 error, render template
    """
    item = db.session.query(Item, Category).filter(Item.cat_id == Category.id,
                                                   Item.item_id == item_id).first()
    if item == None:
        flask.abort(404)
    return render_template("show_item.html", item=item)


@main.route('/profile')
@login_required
def showProfile():
    """
    Function for showing profile
    :return: if user is not confirmed - return auth.unconfirmed else return template with all info
    """
    user = current_user
    if user.confirmed:
        items = db.session.query(Basket, Item, Category).filter(Item.item_id == Basket.item_id) \
            .filter(Item.cat_id == Category.id).filter(Basket.user_id == user.id).all()
        total = 0
        for i in items:
            total += i.Item.item_price * i.Basket.quantity
        return render_template("profile.html", user=user, auth=session.get('auth'), basket=items, total=total)
    else:
        return redirect(url_for('auth.unconfirmed'))


@main.route("/items/<item_id>/basket")
@login_required
def add_item_to_basket(item_id):
    """
    Function for adding item to basket
    :param item_id: id of item
    :return: if user is not confirmed - return auth.unconfirmed else if basket existed - add to it else create basket
    """
    user = current_user
    if user.confirmed:
        existed = Basket.query.filter_by(user_id=user.id, item_id=item_id).first()
        if existed:
            if existed.add_item(item_id):
                db.session.commit()
                return redirect(url_for('main.showProfile'))
            else:
                flash('Ваша ссылка не валидна или истекла!')
        else:
            item = Item.query.filter_by(item_id=item_id)
            if item:
                it = Basket(user_id=user.id, item_id=item_id, quantity=1)
                db.session.add(it)
                db.session.commit()
                return redirect(url_for('main.showProfile'))
            else:
                return flask.abort(404)
    else:
        return redirect(url_for('auth.unconfirmed'))


@main.route("/items/<id_item>/<quantity>/>removefrombasket")
@login_required
def delete_item_from_basket(id_item, quantity):
    """
    Function for deleting item from basket
    :param id_item: id of item
    :param quantity: number of items
    :return: if user is not confirmed - return auth.unconfirmed else if basket is existed and quantity = 1 - remove item
    if quantity = all - delete basket
    """
    user = current_user
    if user.confirmed:
        existed = Basket.query.filter_by(user_id=user.id, item_id=id_item).first()
        if existed:
            if quantity == '1':
                if existed.remove_item(id_item):
                    db.session.commit()
            if quantity == "all" or existed.quantity <= 0:
                Basket.query.filter_by(user_id=user.id, item_id=id_item).delete()
                db.session.commit()
            return redirect(url_for('main.showProfile'))
        else:
            return flask.abort(404)


@main.route('/testForm', methods=['GET', 'POST'])
def testForm():
    """
    Function for testing form
    :return: if everything is right confirm user else - flash mistakes
    """
    text = None
    form = SimpleFrom()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.text.data).first()
        if user is not None:
            if user.password == form.password.data and user.email == form.email.data:
                flash("Thanks for log in!", "success")
                session[
                    'text'] = "Thanks for log in! Your login: " + user.email + " and your password: " + user.password
                form.text.data = ''
                session['auth'] = True
                confirm(user)
                return redirect(url_for('index'))
            else:
                flash("Not correct password or email", "error")
                session['auth'] = False
        else:
            flash("No such user", "warning")
            session['auth'] = False

    return render_template('formTemplate.html', form=form, text=text)


@main.route('/logout')
def logout():
    """
    Function for log out.
    :return: logout user
    """
    if session.get('auth'):
        session['auth'] = False
        session['text'] = None
    return redirect(url_for('main.index'))


def confirm(user):
    """
    Function for confirming user
    :param user: current user
    :return: send mail to user
    """
    send_mail(user.email, 'Create new user', 'send_mail', user=user)


def send_mail(to, subject, template, **kwargs):
    """
    Function for sending email
    :param to: recipient
    :param subject: subject of email
    :param template: template of email
    :param kwargs: other arguments
    :return: send email to user
    """
    msg = Message(subject, sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    mail.send(msg)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    return "For moderator"
