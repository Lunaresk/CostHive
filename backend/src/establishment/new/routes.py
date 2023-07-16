from . import bp
from .forms import NewEstablishmentForm
from src import db, LOGGER
from models import Establishment, LoginToken
from src.utils import database_utils
from src.utils.routes_utils import render_custom_template as render_template
from flask import redirect, url_for
from flask_login import current_user, login_required

@bp.route('/create_establishment', methods=['GET', 'POST'])
@login_required
def create_new_establishment():
    form = NewEstablishmentForm()
    if form.validate_on_submit():
        LOGGER.debug("valid form")
        establishment = Establishment(name=form.name.data, owner=current_user.id)
        db.session.add(establishment)
        db.session.commit()
        new_token = database_utils.generate_token()
        login_token = LoginToken(user=current_user.id, establishment=establishment.id, token=new_token)
        db.session.add(login_token)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('establishment/new/new_establishment.html', form=form)
