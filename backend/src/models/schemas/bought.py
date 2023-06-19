from src import ma
from src.models import Bought
from src.models.schemas import LoginTokenSchema, ItemSchema


class BoughtSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bought
        include_fk = True

    LoginToken = ma.Nested(LoginTokenSchema)
    Item = ma.Nested(ItemSchema)
    date = ma.auto_field()
    amount = ma.auto_field()
