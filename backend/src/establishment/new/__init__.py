from flask import Blueprint

bp = Blueprint("new", __name__, url_prefix='new')

from . import forms, routes