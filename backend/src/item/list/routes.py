from flask import abort, current_app, request
from flask_login import current_user, login_required
from . import bp
from src.models import Item
from src.models.schemas import ItemSchema
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/show_items', methods=['GET', 'POST'])
@login_required
def show_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.id.asc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    if current_user.is_anonymous:
        abort(403)
    return render_template('item/list/show_items.html', items = items)