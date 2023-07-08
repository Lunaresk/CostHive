from src import ma
from ..payment import Payment
from .login_token import LoginTokenSchema


class PaymentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Payment
        include_fk = True

    id = ma.auto_field()
    LoginToken = ma.Nested(LoginTokenSchema)
    date = ma.auto_field()
    amount = ma.auto_field()
