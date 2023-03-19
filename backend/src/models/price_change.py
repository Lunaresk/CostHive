from src import db
from datetime import date

class PriceChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True, server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True, server_default=str(date(2021, 12, 1)))
    price = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Price_Change {self.item} ({self.date})>"