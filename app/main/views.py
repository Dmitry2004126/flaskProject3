import random

from flask import request, make_response, render_template, flash, redirect, url_for, session
from app.main.forms import SimpleFrom
from ..decorators import admin_required, permission_required
from app.models import User, Permission
from flask_mail import Message
from .. import mail
from . import main
from app import db
from flask_login import login_required


@main.route("/check")
def cookie():
    user_agent = request.headers.get('User-Agent')
    if user_agent.lower().__contains__("mozilla"):
        response = make_response("<H1>Everything is good!<H1>")
        response.set_cookie('flag', str(random.randint(1, 100)))
        return response
    else:
        return "<H1>Everything is bad!<H1>"


@main.route("/index/<name>/<city>")
def town(name, city):
    return "<h1>Hello, {}. Yoa are from {}!<h1>".format(name, city)


@main.route("/error")
def error():
    return page_not_found(error)


@main.route('/')
@main.route('/index')
def index():
    default_user = {"username": "Alex"}
    session_text = session.get('text')
    if session_text is not None or session_text != "":
        return render_template("index.html", text=session_text)
    else:
        return render_template('index.html', user=default_user)





@main.route('/testForm', methods=['GET', 'POST'])
def testForm():
    text = None
    form = SimpleFrom()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.text.data).first()
        if user is not None:
            if user.password == form.password.data and user.email == form.email.data :
                flash("Thanks for log in!", "success")
                session['text'] = "Thanks for log in! Your login: " + user.email + " and your password: " + user.password
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
    if session.get('auth'):
        session['auth'] = False
        session['text'] = None
    return redirect(url_for('main.index'))

def confirm(user):
    send_mail(user.email , 'Create new user', 'send_mail', user=user)

def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template+".txt", **kwargs)
    mail.send(msg)


@main.route('/admin')
@login_required
@admin_required
def for_admin():
    return "For admin"


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    return "For moderator"


@main.route("/secret")
@login_required
def secret():
    return "Only for auth"


@main.route("/testConfirm")
def testConfirm():
    user = User.query.filter_by().first()
    tmp = user.generate_confirmation_token()
    user.confirm(tmp)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)