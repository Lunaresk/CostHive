from flask import Blueprint

bp = Blueprint('receipts', __name__, url_prefix='/receipts')
from .upload import bp as bp_upload
bp.register_blueprint(bp_upload)
from .check_items import bp as bp_check_items
bp.register_blueprint(bp_check_items)