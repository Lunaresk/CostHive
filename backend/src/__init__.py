from configs.config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
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
cors = CORS()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.web_login'
ma = Marshmallow()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
    app.config.from_object(config_class)
    bootstrap.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    login.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from src.main import bp as main_bp
    app.register_blueprint(main_bp)
    from src.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from src.errors import bp as error_bp
    app.register_blueprint(error_bp)
    from src.api import bp as api_bp
    app.register_blueprint(api_bp)
    from src.receipts import bp as receipts_bp
    app.register_blueprint(receipts_bp)
    from src.item import bp as item_bp
    app.register_blueprint(item_bp)
    from src.establishment import bp as establishment_bp
    app.register_blueprint(establishment_bp)
    
    return app

from models import *