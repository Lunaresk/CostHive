from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from yaml import safe_load

app = Flask(__name__)
app.config.from_file("config.yaml", safe_load)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)

from app import views, models