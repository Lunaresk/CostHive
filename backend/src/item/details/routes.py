# from flask_login import login_required
from . import bp
from models import Item
from models.schemas import ItemSchema
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/<item>', methods=['GET'])
def show_item(item: int):
    itemobj = Item.query.get_or_404(item)
    itemschema = ItemSchema().dump(itemobj)
    itemschema['PriceChange'].sort(key=lambda d: d['date'], reverse=True)
    itemschema['AmountChange'].sort(key=lambda d: d['date'], reverse=True)
    print(itemschema)
    return render_template('item/details/show_item.html', item = itemschema)