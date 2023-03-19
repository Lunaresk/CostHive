from flask import Blueprint

bp = Blueprint('establishment', __name__, url_prefix='/establishment')
from src.establishment.new import bp as bp_new
bp.register_blueprint(bp_new)
from src.establishment.list import bp as bp_list
bp.register_blueprint(bp_list)
from src.establishment.overview import bp as bp_overview
bp.register_blueprint(bp_overview)
from src.establishment.candidates import bp as bp_candidates
bp.register_blueprint(bp_candidates)