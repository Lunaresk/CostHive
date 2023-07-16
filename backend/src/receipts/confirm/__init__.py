from flask import Blueprint

bp = Blueprint('confirm', __name__, url_prefix='/confirm')

from . import forms, routes