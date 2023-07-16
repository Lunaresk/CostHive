# from src import db, LOGGER
from flask import abort, current_app, redirect, request, url_for
from flask_login import current_user
from . import bp
from .forms import JoinEstablishmentForm
from .utils import backend_validation
from src import db
from models import Establishment
from models import EstablishmentCandidate
from src.utils.routes_utils import render_custom_template as render_template


@bp.route('/show_establishments', methods=["GET", "POST"])
def show_establishments():
    page = request.args.get('page', 1, type=int)
    establishments = Establishment.query.order_by(Establishment.id.asc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    if current_user.is_authenticated:
        form = JoinEstablishmentForm()
        if (form.validate_on_submit()):
            if (backend_validation(form)):
                establishment_candidate = EstablishmentCandidate(
                    user=current_user.id, establishment=form.id.data)
                db.session.add(establishment_candidate)
                db.session.commit()
                return redirect(url_for('establishment.list.show_establishments'))
            return abort(403)
        return render_template("establishment/list/establishment_list.html", establishments=establishments.items, form=form)
    return render_template("establishment/list/establishment_list.html", establishments=establishments.items)
