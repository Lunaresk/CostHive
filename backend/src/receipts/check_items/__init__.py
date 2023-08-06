from flask import Blueprint

bp = Blueprint('check_items', __name__, url_prefix='/check_items')

from . import forms, routes