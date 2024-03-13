import random

from flask import request, make_response, render_template, flash, redirect, url_for, session
from app.forms import SimpleFrom
from app import app



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
        return render_template("index.html", text=session_text)
    else:
        return render_template('index.html', user=default_user)



@app.errorhandler(400)
def page_not_found(e):
    return render_template("404.html"), 400


@app.route('/testForm', methods=['GET', 'POST'])
def testForm():
    text = None
    form = SimpleFrom()

    if form.validate_on_submit():
        flash("Thanks for registration!", "success")
        session['text'] = "Thanks for registration! Your login: " + form.text.data + " and your email: " + form.email.data
        form.text.data = ''
        return redirect(url_for('index'))
    return render_template('formTemplate.html', form=form, text=text)
