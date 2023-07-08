from src import db


class ReceiptItem(db.Model):
    receipt = db.Column(db.ForeignKey("receipt.id"),
                        primary_key=True, server_onupdate=db.FetchedValue())
    item = db.Column(db.ForeignKey("item.id"), primary_key=True,
                     server_onupdate=db.FetchedValue())
    amount = db.Column(db.SmallInteger, nullable=False)
    accepted = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"<ReceiptItem {self.receipt}: {self.item}>"
