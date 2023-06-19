from src import db


class EstablishmentCandidate(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True)
    establishment = db.Column(db.ForeignKey(
        'establishment.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"<EstablishmentCandidate {self.user} ({self.establishment})>"
