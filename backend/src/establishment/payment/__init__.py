from flask import Blueprint

bp = Blueprint('payment', __name__, url_prefix='/payment')

from src.establishment.payment import routes