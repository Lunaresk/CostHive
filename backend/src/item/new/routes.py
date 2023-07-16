from datetime import date
from flask import abort, redirect, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import NewItemForm
from src import db, LOGGER
from models import AmountChange, Brand, Item, PriceChange
from src.utils.routes_utils import render_custom_template as render_template

@bp.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    if current_user.is_anonymous:
        abort(403)
    form = NewItemForm.new()
    if form.is_submitted():
        LOGGER.debug("submitted")
    if form.validate():
        LOGGER.debug("valid")
    else:
        LOGGER.debug(form.errors)
    if form.validate_on_submit():
        LOGGER.debug("valid form")
        brand = Brand.query.get(form.brand.data)
        new_item = Item(id=form.id.data, name=form.name.data,
                        brand=brand.id, description=form.description.data)
        # if form.category.data:
        #     category = Category.query.get(id = form.category.data)
        #     new_item.Category = category
        new_item.PriceChange = [PriceChange(Item=new_item, date=date(
            2021, 12, 1), price=form.price_change.data)]
        if form.amount_change.data:
            new_item.AmountChange = [AmountChange(Item=new_item, date=date(
                2021, 12, 1), amount=form.amount_change.data)]
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('item/new/new_item.html', form=form)