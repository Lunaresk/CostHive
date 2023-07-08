from datetime import date
from src import db


class AmountChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True,
                     server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True,
                     server_default=str(date(2021, 12, 1)))
    amount = db.Column(db.SmallInteger, nullable=False, server_default=str(1))

    def __repr__(self) -> str:
        return f"<Amount_Change {self.item} ({self.date})>"
