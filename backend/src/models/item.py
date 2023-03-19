from src import db
from src.models.item_category import item_category

class Item(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.ForeignKey('brand.id'), nullable=False, server_onupdate=db.FetchedValue())
    description = db.Column(db.Text, nullable=False)

    AmountChange = db.relationship("AmountChange", backref='Item', lazy='dynamic')
    Bought = db.relationship("Bought", backref='Item', lazy='dynamic')
    Category = db.relationship("Category", secondary=item_category, lazy="dynamic", back_populates="Item")
    PriceChange = db.relationship("PriceChange", backref='Item', lazy='dynamic')
    ReceiptItem = db.relationship("ReceiptItem", backref='Item', lazy='dynamic')
    
    def __repr__(self) -> str:
        return f"<Item {self.id} ({self.name})>"