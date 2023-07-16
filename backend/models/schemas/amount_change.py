from src import ma
from ..amount_change import AmountChange
from .item import ItemSchema

    
class AmountChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AmountChange
        include_fk = True

    Item = ma.Nested(ItemSchema)
    date = ma.auto_field()
    amount = ma.auto_field()