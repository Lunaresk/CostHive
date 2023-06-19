from flask import abort, redirect, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import EvaluateCandidateForm
from src import db, LOGGER
from src.models import Establishment, EstablishmentCandidate, LoginToken, User
from src.utils.routes_utils import render_custom_template as render_template
from src.utils.database_utils import generate_token

@bp.route("/<establishment_id>", methods=["GET", "POST"])
@login_required
def candidates(establishment_id):
    establishment = Establishment.query.get_or_404(establishment_id)
    if(current_user == establishment.User):
        form = EvaluateCandidateForm()
        establishment_candidates = EstablishmentCandidate.query.filter_by(establishment = establishment.id).all()
        if(form.validate_on_submit()):
            if(form.accept.data):
                login_token = LoginToken(Establishment = establishment, User = User.query.get(form.candidate_id.data), token = generate_token())
                db.session.add(login_token)
            establishment_candidate = EstablishmentCandidate.query.filter_by(establishment = establishment.id, user = form.candidate_id.data).first()
            db.session.delete(establishment_candidate)
            db.session.commit()
            return redirect(url_for('.candidates', establishment_id = establishment_id))
        return render_template("establishment/candidates/candidates.html", establishment_candidates=establishment_candidates, form=form)
    abort(403)