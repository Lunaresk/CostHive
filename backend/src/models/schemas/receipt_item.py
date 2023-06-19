from src import ma
from src.models import ReceiptItem
from src.models.schemas import ItemSchema, ReceiptSchema


class ReceiptItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReceiptItem
        include_fk = True

    Receipt = ma.Nested(ReceiptSchema)
    Item = ma.Nested(ItemSchema)
    amount = ma.auto_field()
    accepted = ma.auto_field()
