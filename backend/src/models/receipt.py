from src import db


class Receipt(db.Model):
    id = db.Column(db.Numeric(precision=24, scale=0),
                   primary_key=True, autoincrement=False)
    date = db.Column(db.Date, nullable=False)
    from_user = db.Column(db.ForeignKey("login_token.token"),
                          server_onupdate=db.FetchedValue())
    registered = db.Column(db.Boolean, nullable=False,
                           server_default=str(False))

    ReceiptItem = db.relationship(
        "ReceiptItem", backref='Receipt', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<Receipt {self.id}>"
