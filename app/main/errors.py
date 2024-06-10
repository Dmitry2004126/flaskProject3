from flask import render_template
from . import main


@main.errorhandler(400)
def page_not_found(error):
    return render_template("404.html"), 400
