import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from flask import Flask
from flask_bootstrap import Bootstrap5

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = "hard to unlock"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_proj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)

from models import *
migrate = Migrate(app, db)

from app import routes



