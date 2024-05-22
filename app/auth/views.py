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
        if current_user.confirmed and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
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
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)

        user.set_password(form.password.data)
        print(user.email)
        db.session.add(user)
        print(user.password_verify("pass"))
        db.session.commit()
        token = user.generate_confirmation_token()
        send_confirm(user, token)
        print(user.password_verify("pass"))
        flash("registr complete!")
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash("Good")
    else:
        flash("Bad")
    return redirect(url_for('main.index'))


def send_confirm(user, token):
    send_mail(user.email, 'Create your account', 'auth/confirm', user=user, token=token.decode('utf-8'))
    redirect(url_for('main.index'))


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender="ttestovich271@gmail.com",
                  recipients=[to])
    try:

        msg.html = render_template(template + ".html", **kwargs)
    except:
        msg.body = render_template(template + ".txt", **kwargs)
    from app_file import app
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/unconfirmed.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logout")
    return redirect((url_for("main.index")))
