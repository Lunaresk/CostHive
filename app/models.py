from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

item_category = db.Table("item_category",
    db.Column("item", db.ForeignKey("item.id"), primary_key=True),
    db.Column("category", db.ForeignKey("category.id"), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    Bought = db.relationship("Bought", backref='User', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.name})>"

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self) -> str:
        return f"<Brand {self.id} ({self.name})>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    Item = db.relationship("Item", secondary=item_category, lazy="dynamic", back_populates="Category")
    
    def __repr__(self) -> str:
        return f"<Category {self.id} ({self.name})>"

class Item(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64))
    brand = db.Column(db.ForeignKey('brand.id'))
    description = db.Column(db.Text)

    Category = db.relationship("Category", secondary=item_category, lazy="dynamic", back_populates="Item")

    Item = db.relationship("Bought", backref='Item', lazy='dynamic')
    
    def __repr__(self) -> str:
        return f"<Item {self.id} ({self.name})>"

class Bought(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True)
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.SmallInteger)


    
    def __repr__(self) -> str:
        return f"<Bought Object>"

class PriceChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    price = db.Column(db.SmallInteger)
    
    def __repr__(self) -> str:
        return f"<Price_Change {self.item} ({self.date})>"

class AmountChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger)
    
    def __repr__(self) -> str:
        return f"<Amount_Change {self.item} ({self.date})>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))