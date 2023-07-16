from src import ma
from ..login_token import LoginToken
from .establishment import EstablishmentSchema
from .user import UserSchema


class LoginTokenSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LoginToken
        include_fk = True

    User = ma.Nested(UserSchema)
    Establishment = ma.Nested(EstablishmentSchema)
    token = ma.auto_field()
