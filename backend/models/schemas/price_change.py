from src import ma
from .item import ItemSchema
from ..price_change import PriceChange

class PriceChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PriceChange
        include_fk = True

    Item = ma.Nested(ItemSchema)
    date = ma.auto_field()
    price = ma.auto_field()
