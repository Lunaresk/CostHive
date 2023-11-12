from src import ma
from ..receipt_item import ReceiptItem
from .item import ItemSchema
from .receipt import ReceiptSchema


class ReceiptItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReceiptItem
        include_fk = True

    Receipt = ma.Nested(ReceiptSchema)
    price = ma.auto_field()
    amount = ma.auto_field()
