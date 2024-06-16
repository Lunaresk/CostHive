from src import db


class Payment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    token = db.Column(db.ForeignKey('login_token.token'),
                      server_onupdate=db.FetchedValue(), nullable=False)
    date = db.Column(db.Date, nullable=False, server_default=db.func.now())
    amount = db.Column(db.BigInteger, nullable=False, server_default=str(0))

    def __repr__(self) -> str:
        return f"<Payment {self.id}>"
