from flask import jsonify
from src.main import bp
from src.utils.routes_utils import render_custom_template as render_template
from src.models import User, UserSchema

@bp.route('/')
@bp.route('/index')
def index():
    return render_template("base.html")

@bp.route('/test')
def test():
    user_objects = User.query.all()
    schema = UserSchema(many = True)
    users = schema.dump(user_objects)
    return jsonify(users)