import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = "hard to unlock"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_proj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ttestovich271@gmail.com'
app.config['MAIL_PASSWORD'] = 'uvke dpsj gczk mdbk'

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
mail = Mail(app)

from models import *
migrate = Migrate(app, db)

from app import routes



