from flask import render_template
from . import main


@main.errorhandler(400)
def page_not_found(e):
    return render_template("404.html"), 400
