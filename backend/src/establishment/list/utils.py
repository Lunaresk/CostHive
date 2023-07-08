from flask_login import current_user
from models import Establishment


def backend_validation(join_establishment_form):
    establishment = Establishment.query.get(join_establishment_form.id.data)
    return not (establishment.LoginToken.filter_by(user=current_user.id).first() or current_user.EstablishmentCandidate.filter_by(establishment=join_establishment_form.id.data).first())
