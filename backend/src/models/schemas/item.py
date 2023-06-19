from src import ma
from src.models import Item
from src.models.schemas import BrandSchema


class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Item
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    Brand = ma.Nested(BrandSchema)
