from flask import Blueprint

bp = Blueprint('v1', __name__, url_prefix='/v1')

from . import routes