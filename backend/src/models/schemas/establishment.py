from src import ma
from src.models import Establishment
from src.models.schemas import UserSchema


class EstablishmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Establishment
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    User = ma.Nested(UserSchema)
