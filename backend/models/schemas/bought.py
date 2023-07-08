from src import ma
from ..bought import Bought
from .login_token import LoginTokenSchema
from .item import ItemSchema


class BoughtSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bought
        include_fk = True

    LoginToken = ma.Nested(LoginTokenSchema)
    Item = ma.Nested(ItemSchema)
    date = ma.auto_field()
    amount = ma.auto_field()
