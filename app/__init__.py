from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from yaml import safe_load
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

if not exists(DIR + "logs"):
    makedirs(DIR + "logs")

fileConfig(DIR + "configs/log.conf")
LOGGER = getLogger("root")

app = Flask(__name__)
app.config.from_file("configs/config.yaml", safe_load)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'web_login'

from app import routes, models