from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from .v1 import bp as bp_v1
bp.register_blueprint(bp_v1)