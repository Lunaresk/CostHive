from flask import Blueprint

bp = Blueprint("candidates", __name__, url_prefix='candidates')

from . import forms, routes