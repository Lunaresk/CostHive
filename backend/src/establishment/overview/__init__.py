from flask import Blueprint

bp = Blueprint('overview', __name__, url_prefix='/overview')

from src.establishment.overview import routes