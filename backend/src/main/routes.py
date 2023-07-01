from . import bp
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/')
@bp.route('/index')
def index():
    return render_template("base.html")

@bp.route('/test', methods=["GET", "POST"])
def test():
    return "Hello Test"