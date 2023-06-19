from src import ma
from src.models import AmountChange
from src.models.schemas import ItemSchema

    
class AmountChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AmountChange
        include_fk = True

    Item = ma.Nested(ItemSchema)
    date = ma.auto_field()
    amount = ma.auto_field()