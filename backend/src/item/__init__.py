from flask import Blueprint

bp = Blueprint('item', __name__, url_prefix='/item')
from .new import bp as bp_new_item
bp.register_blueprint(bp_new_item)
from .list import bp as bp_item_list
bp.register_blueprint(bp_item_list)
from .details import bp as bp_item_details
bp.register_blueprint(bp_item_details)
from .update import bp as bp_item_update
bp.register_blueprint(bp_item_update)