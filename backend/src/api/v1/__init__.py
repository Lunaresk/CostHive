from flask import Blueprint

bp = Blueprint('v1', __name__, url_prefix='/v1')

from src.api.v1 import routes