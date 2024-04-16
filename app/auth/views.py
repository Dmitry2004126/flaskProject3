from flask import render_template, redirect, request, flash, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from flask_login import login_user, login_required, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):

            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):

                next = url_for('main.index')
            return redirect(next)
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
        print(user.password_verify("pass"))
        flash("registr complete!")
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logout")
    return redirect((url_for("main.index")))