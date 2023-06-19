from flask import abort, redirect, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import NewPaymentForm
from src import db, LOGGER
from src.models import Establishment, Payment
from src.utils.routes_utils import render_custom_template as render_template


@bp.route('/<int:establishment_id>', methods=['GET', 'POST'])
@login_required
def insert_payment(establishment_id: int):
    establishment = Establishment.query.get(int(establishment_id))
    if current_user.is_anonymous or current_user.id != establishment.owner:
        abort(403)
    form = NewPaymentForm.new(establishment_id=establishment_id)
    if form.validate_on_submit():
        new_payment = Payment(token = form.token.data,
                          date = form.date.data,
                          amount = form.amount.data)
        db.session.add(new_payment)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template('establishment/payment/new_payment.html', form=form)