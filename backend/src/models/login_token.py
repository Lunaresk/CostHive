from src import db

class LoginToken(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True, server_onupdate=db.FetchedValue())
    establishment = db.Column(db.ForeignKey('establishment.id'), primary_key=True, server_onupdate=db.FetchedValue())
    token = db.Column(db.String(15), nullable=False, unique=True)

    Payment = db.relationship("Payment", backref='LoginToken', lazy='dynamic')
    Receipt = db.relationship("Receipt", backref='LoginToken', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<LoginToken {self.token}>"