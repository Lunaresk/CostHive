from configs.config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from logging import getLogger
from logging.config import fileConfig
from os import makedirs
from os.path import dirname, exists

try:
    dir_name = dirname(__file__)
    if dir_name:
        DIR = dir_name + "/"
    else:
        DIR = "./"
except NameError:
    DIR = "./"

if not exists(DIR + "../logs"):
    makedirs(DIR + "../logs")

fileConfig(DIR + "../configs/log.conf")
LOGGER = getLogger("main")

bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.web_login'
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/error')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    from app.receipts import bp as receipts_bp
    app.register_blueprint(receipts_bp, url_prefix='/receipts')

    return app

from app import models