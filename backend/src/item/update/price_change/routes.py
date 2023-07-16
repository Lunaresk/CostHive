from flask import abort, redirect, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import NewPriceChangeForm
from src import db, LOGGER
from models import Item, PriceChange
from src.utils.routes_utils import render_custom_template as render_template


@bp.route('/<int:item>', methods=['GET', 'POST'])
@login_required
def price_change(item: int):
    if current_user.is_anonymous:
        abort(403)
    db_item = Item.query.get_or_404(item)
    form = NewPriceChangeForm()
    form.id.data = int(item)
    if form.validate_on_submit():
        db_price_change = PriceChange(
            item=form.id.data, date=form.date.data, price=form.price_change.data)
        db.session.add(db_price_change)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('item/update/price_change/price_change.html', form=form, item=db_item)
