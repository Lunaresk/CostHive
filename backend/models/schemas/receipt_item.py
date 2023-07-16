from src import ma
from ..receipt_item import ReceiptItem
from .item import ItemSchema
from .receipt import ReceiptSchema


class ReceiptItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReceiptItem
        include_fk = True

    Receipt = ma.Nested(ReceiptSchema)
    Item = ma.Nested(ItemSchema)
    amount = ma.auto_field()
    accepted = ma.auto_field()
