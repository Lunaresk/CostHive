from src import ma
from src.models import Payment
from src.models.schemas import LoginTokenSchema


class PaymentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Payment
        include_fk = True

    id = ma.auto_field()
    LoginToken = ma.Nested(LoginTokenSchema)
    date = ma.auto_field()
    amount = ma.auto_field()
