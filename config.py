import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hard to unlock"
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.googlemail.com"
    MAIL_PORT = os.environ.get('MAIL_PORT') or "587"
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', '5870'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "ttestovich271@gmail.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "uvke dpsj gczk mdbk"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_ADMIN = "test2@test.ru"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:@localhost/flask_proj2'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:@localhost/flask_proj2'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:@localhost/flask_proj2'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
