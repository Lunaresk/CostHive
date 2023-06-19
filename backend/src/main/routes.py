from flask import jsonify, request
from . import bp
from src.models import User
from src.models.schemas import UserSchema
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/')
@bp.route('/index')
def index():
    return render_template("base.html")

@bp.route('/test')
def test():
    print(request.content_type)
    user_objects = User.query.all()
    schema = UserSchema(many = True)
    users = schema.dump(user_objects)
    return jsonify(users)