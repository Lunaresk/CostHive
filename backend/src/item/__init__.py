from flask import Blueprint

bp = Blueprint('item', __name__, url_prefix='/item')
from src.item.new import bp as bp_new_item
bp.register_blueprint(bp_new_item)