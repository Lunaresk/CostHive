# from marshmallow import Schema, fields
from src import ma
from ..category import Category


class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Category

    id = ma.auto_field()
    name = ma.auto_field()
