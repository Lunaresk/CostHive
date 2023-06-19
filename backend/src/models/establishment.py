from src import db


class Establishment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    owner = db.Column(db.ForeignKey('user.id'), nullable=False)

    LoginToken = db.relationship(
        "LoginToken", backref='Establishment', lazy='dynamic')
    Bought = db.relationship("Bought", secondary="login_token",
                             lazy='dynamic', overlaps="Establishment,LoginToken,Bought")
    EstablishmentCandidate = db.relationship(
        "EstablishmentCandidate", backref='Establishment', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<Establishment {self.id} ({self.name})>"
