from src import ma
from ..establishment_candidate import EstablishmentCandidate
from .establishment import EstablishmentSchema
from .user import UserSchema


class EstablishmentCandidateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EstablishmentCandidate
        include_fk = True

    User = ma.Nested(UserSchema)
    Establishment = ma.Nested(EstablishmentSchema)
