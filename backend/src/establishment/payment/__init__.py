from flask import Blueprint

bp = Blueprint('payment', __name__, url_prefix='/payment')

from . import forms, routes