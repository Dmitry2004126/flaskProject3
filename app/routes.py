import random

from flask import request, make_response, render_template
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
    user = {"username": "Alex"}
    return render_template("index.html", user=user)


@app.errorhandler(400)
def page_not_found(e):
    return render_template("404.html"), 400

