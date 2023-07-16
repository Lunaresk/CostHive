from src import ma
from ..item import Item
from .brand import BrandSchema

class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Item
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    Brand = ma.Nested(BrandSchema)
    PriceChange = ma.List(ma.Nested(lambda: PriceChangeSchema(exclude=("Item",))))
    AmountChange = ma.List(ma.Nested(lambda: AmountChangeSchema(exclude=("Item",))))

from .price_change import PriceChangeSchema
from .amount_change import AmountChangeSchema