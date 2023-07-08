from flask import Blueprint

bp = Blueprint('amount_change', __name__, url_prefix='/amount_change')

from . import forms, routes