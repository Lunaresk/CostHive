from flask import Blueprint

bp = Blueprint('receipts', __name__, url_prefix='/receipts')

from . import forms, routes