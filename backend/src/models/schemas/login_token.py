from src import ma
from src.models import LoginToken
from src.models.schemas import EstablishmentSchema, UserSchema


class LoginTokenSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LoginToken
        include_fk = True

    User = ma.Nested(UserSchema)
    Establishment = ma.Nested(EstablishmentSchema)
    token = ma.auto_field()
