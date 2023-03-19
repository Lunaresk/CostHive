from src import db

class Bought(db.Model):
    token = db.Column(db.ForeignKey('login_token.token'), primary_key=True, server_onupdate=db.FetchedValue())
    item = db.Column(db.ForeignKey('item.id'), primary_key=True, server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    registered = db.Column(db.Boolean, nullable=False, server_default=str(False))

    def __repr__(self) -> str:
        return f"<Bought Object>"