from flask import jsonify
from . import bp
from src.models import User
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/')
@bp.route('/index')
def index():
    return render_template("base.html")