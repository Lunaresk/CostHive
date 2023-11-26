from src import db


class ReceiptItem(db.Model):
    receipt = db.Column(db.ForeignKey("receipt.id"),
                        primary_key=True, server_onupdate=db.FetchedValue())
    item = db.Column(db.SmallInteger, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.SmallInteger, nullable=False, default=str(1))
    price = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self) -> str:
        return f"<ReceiptItem {self.receipt}: {self.item}>"
