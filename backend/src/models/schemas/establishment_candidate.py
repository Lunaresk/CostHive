from src import ma
from src.models import EstablishmentCandidate
from src.models.schemas import EstablishmentSchema, UserSchema


class EstablishmentCandidateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EstablishmentCandidate
        include_fk = True

    User = ma.Nested(UserSchema)
    Establishment = ma.Nested(EstablishmentSchema)
