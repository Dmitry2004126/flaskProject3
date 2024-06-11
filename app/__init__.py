from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from config import config
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate

bootstrap = Bootstrap5()
db = SQLAlchemy()
mail = Mail()
oauth = OAuth()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'auth.login'


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 3


admin = Admin(index_view=CustomAdminIndexView())


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


from app.main import views
