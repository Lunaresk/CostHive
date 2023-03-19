# from src import db, LOGGER
from flask import abort, current_app, redirect, request, url_for
from flask_login import current_user
from src import db
from src.models import Establishment
from src.establishment.list import bp
from src.establishment.list.forms import JoinEstablishmentForm
from src.establishment.list.utils import backend_validation
from src.models import EstablishmentCandidate
from src.utils.routes_utils import render_custom_template as render_template


@bp.route('/show_establishments', methods=["GET", "POST"])
def show_establishments():
    page = request.args.get('page', 1, type=int)
    establishments = Establishment.query.order_by(Establishment.id.asc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for(".show_establishments",
                       page=establishments.next_num) if establishments.has_next else None
    prev_url = url_for(".show_establishments",
                       page=establishments.prev_num) if establishments.has_prev else None
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
        return render_template("establishment/list/establishment_list.html", establishments=establishments.items, form=form, next_url=next_url, prev_url=prev_url)
    return render_template("establishment/list/establishment_list.html", establishments=establishments.items, next_url=next_url, prev_url=prev_url)
