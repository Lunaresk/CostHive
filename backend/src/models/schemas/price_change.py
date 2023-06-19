from src import ma
from src.models import PriceChange
from src.models.schemas import ItemSchema


class PriceChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PriceChange
        include_fk = True

    Item = ma.Nested(ItemSchema)
    date = ma.auto_field()
    price = ma.auto_field()
