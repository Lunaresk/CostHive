from flask import Blueprint

bp = Blueprint('update', __name__, url_prefix='/update')
from .price_change import bp as bp_price_change
bp.register_blueprint(bp_price_change)
from .amount_change import bp as bp_amount_change
bp.register_blueprint(bp_amount_change)