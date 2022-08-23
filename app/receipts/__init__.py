from flask import Blueprint

bp = Blueprint('receipts', __name__)

from app.receipts import forms, routes