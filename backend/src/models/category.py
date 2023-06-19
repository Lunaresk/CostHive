from src import db
from src.models.item_category import item_category


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)

    Item = db.relationship("Item", secondary=item_category,
                           lazy="dynamic", back_populates="Category")

    def __repr__(self) -> str:
        return f"<Category {self.id} ({self.name})>"
