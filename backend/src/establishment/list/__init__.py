from flask import Blueprint

bp = Blueprint("list", __name__, url_prefix='list')

from . import routes