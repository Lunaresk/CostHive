from src import db


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)

    Item = db.relationship("Item", backref='Brand', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<Brand {self.id} ({self.name})>"

    def __str__(self) -> str:
        return f"{self.name}"
