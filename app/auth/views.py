from flask import render_template, redirect, request, flash, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from threading import Thread
from app import mail


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Function for user to sign in
    :return if form is submitted and password is right and email is confirmed - main.index, else auth.unconfirmed
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user)
            if not user.confirmed:
                return redirect(url_for("auth.unconfirmed"))
            return redirect(url_for("main.index"))
        flash('Invalid username or password')
    return render_template("auth/login.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Function for user to sign up
    :return: if form is submitted redirect to auth.login else render template
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        db.session.add(user)
        user.set_password = form.password.data
        db.session.commit()
        token = user.generate_confirmation_token()
        send_confirm(user, token)
        flash("registr complete!")
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Function for checking token of user
    :param token: generated token for user
    :return: if user is confirmed return main.index, if token is correct - user is confirmed and flash good
    else flash bad.
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash("Good")
    else:
        flash("Bad")
    return redirect(url_for('main.index'))


def send_confirm(user, token):
    """
    Function for giving all information for email
    :param user: recipient of email
    :param token: generated token for user
    :return: calls send_mail and redirect to main.index
    """
    send_mail(user.email, 'Create your account', 'auth/confirm', user=user, token=token.decode('utf-8'))
    redirect(url_for('main.index'))


def send_mail(to, subject, template, **kwargs):
    """
    Function for creating an email
    :param to: recipient
    :param subject: subject of email
    :param template: template of email
    :param kwargs: other arguments
    :return: thread for async sending of email
    """
    msg = Message(subject, sender="ttestovich271@gmail.com", recipients=[to])
    try:
        msg.html = render_template(template + ".html", **kwargs)
    except:
        msg.body = render_template(template + ".txt", **kwargs)
    from app_file import app
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread


def send_async_email(app, msg):
    """
    Function for sending an email
    :param app: curr app
    :param msg: the mail
    :return: send mail
    """
    with app.app_context():
        mail.send(msg)


@auth.route('/unconfirmed')
def unconfirmed():
    """
    Function for unconfirmed user
    :return: if user is anonymous or confirmed - redirect to main.index else render auth/unconfirmed.html
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/unconfirmed.html')


@auth.route("/logout")
@login_required
def logout():
    """
    Function for log out
    :return: user log out and redirect for main.index
    """
    logout_user()
    flash("You are logout")
    return redirect((url_for("main.index")))
