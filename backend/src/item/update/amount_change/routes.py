from flask import abort, redirect, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import NewAmountChangeForm
from src import db, LOGGER
from models import AmountChange, Item
from src.utils.routes_utils import render_custom_template as render_template


@bp.route('/<int:item>', methods=['GET', 'POST'])
@login_required
def amount_change(item: int):
    if current_user.is_anonymous:
        abort(403)
    db_item = Item.query.get_or_404(item)
    form = NewAmountChangeForm()
    form.id.data = item
    if form.validate_on_submit():
        db_amount_change = AmountChange(
            item=form.id.data, date=form.date.data, amount=form.amount_change.data)
        db.session.add(db_amount_change)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('item/update/amount_change/amount_change.html', form=form, item=db_item)
