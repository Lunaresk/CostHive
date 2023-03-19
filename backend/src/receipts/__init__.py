from flask import Blueprint

bp = Blueprint('receipts', __name__, url_prefix='/receipts')

from src.receipts import forms, routes