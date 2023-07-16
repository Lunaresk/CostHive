from src import ma
from ..receipt import Receipt
from .login_token import LoginTokenSchema


class ReceiptSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Receipt
        include_fk = True

    id = ma.auto_field()
    date = ma.auto_field()
    bonid = ma.auto_field()
    registered = ma.auto_field()
    LoginToken = ma.Nested(LoginTokenSchema)
