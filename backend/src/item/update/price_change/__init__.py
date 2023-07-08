from flask import Blueprint

bp = Blueprint('price_change', __name__, url_prefix='/price_change')

from . import forms, routes