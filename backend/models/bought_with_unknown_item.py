from src import db
from .bought import Bought


class BoughtWithUnknownItem(db.Model):
    token = db.Column(db.ForeignKey('login_token.token'),
                      primary_key=True, server_onupdate=db.FetchedValue())
    item = db.Column(db.BigInteger, primary_key=True,
                     server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self) -> str:
        return f"<Bought Object>"
