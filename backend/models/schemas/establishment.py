from src import ma
from ..establishment import Establishment
from .user import UserSchema


class EstablishmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Establishment
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    User = ma.Nested(UserSchema)
