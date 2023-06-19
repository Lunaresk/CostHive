from src import ma
from src.models import Brand


class BrandSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Brand

    id = ma.auto_field()
    name = ma.auto_field()
