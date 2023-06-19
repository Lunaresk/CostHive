from src import ma
from src.models import Receipt
from src.models.schemas import LoginTokenSchema


class ReceiptSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Receipt
        include_fk = True

    id = ma.auto_field()
    date = ma.auto_field()
    LoginToken = ma.Nested(LoginTokenSchema)
    registered = ma.auto_field()
