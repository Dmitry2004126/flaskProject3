import random

from flask import request, make_response, render_template, flash, redirect, url_for, session
from app.forms import SimpleFrom
from app import app, db
from models import Role, User



@app.route("/check")
def cookie():
    user_agent = request.headers.get('User-Agent')
    if user_agent.lower().__contains__("mozilla"):
        response = make_response("<H1>Everything is good!<H1>")
        response.set_cookie('flag', str(random.randint(1, 100)))
        return response
    else:
        return "<H1>Everything is bad!<H1>"


@app.route("/index/<name>/<city>")
def town(name, city):
    return "<h1>Hello, {}. Yoa are from {}!<h1>".format(name, city)


@app.route("/error")
def error():
    return page_not_found(error)


@app.route('/')
@app.route('/index')
def index():
    default_user = {"username": "Alex"}
    session_text = session.get('text')
    if session_text is not None or session_text != "":
        return render_template("index.html", text=session_text, auth=session.get('auth'))
    else:
        return render_template('index.html', user=default_user, auth=session.get('auth'))



@app.errorhandler(400)
def page_not_found(e):
    return render_template("404.html"), 400


@app.route('/testForm', methods=['GET', 'POST'])
def testForm():
    text = None
    form = SimpleFrom()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.text.data).first()
        if user is not None:
            if user.password == form.password.data :
                flash("Thanks for log in!", "success")
                session['text'] = "Thanks for log in! Your login: " + user.email + " and your password: " + user.password
                form.text.data = ''
                session['auth'] = True
                return redirect(url_for('index'))
            else:
                flash("Not correct password", "error")
                session['auth'] = False
        else:
            flash("No such user", "warning")
            session['auth'] = False

    return render_template('formTemplate.html', form=form, text=text, auth=session.get('auth'))

@app.route('/logout')
def logout():
    if session.get('auth'):
        session['auth'] = False
        session['text'] = None
    return redirect(url_for('index'))