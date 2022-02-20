from app import db, login
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

item_category = db.Table("item_category",
    db.Column("item", db.ForeignKey("item.id"), primary_key=True),
    db.Column("category", db.ForeignKey("category.id"), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Bought = db.relationship("Bought", backref='User', lazy='dynamic')
    LoginToken = db.relationship("LoginToken", backref='User', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.username})>"

class Establishment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    LoginToken = db.relationship("LoginToken", backref='Establishment', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<Establishment {self.id} ({self.name})>"

class LoginToken(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True)
    establishment = db.Column(db.ForeignKey('establishment.id'), primary_key=True)
    token = db.Column(db.String(15), nullable=True, unique=True)

    def __repr__(self) -> str:
        return f"LoginToken {self.token}"

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return f"<Brand {self.id} ({self.name})>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)

    Item = db.relationship("Item", secondary=item_category, lazy="dynamic", back_populates="Category")
    
    def __repr__(self) -> str:
        return f"<Category {self.id} ({self.name})>"

class Item(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.ForeignKey('brand.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)

    Category = db.relationship("Category", secondary=item_category, lazy="dynamic", back_populates="Item")
    Bought = db.relationship("Bought", backref='Item', lazy='dynamic')
    PriceChange = db.relationship("PriceChange", backref='Item', lazy='dynamic')
    AmountChange = db.relationship("AmountChange", backref='Item', lazy='dynamic')
    
    def __repr__(self) -> str:
        return f"<Item {self.id} ({self.name})>"

class Bought(db.Model):
    token = db.Column(db.ForeignKey('login_token.token'), primary_key=True)
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    registered = db.Column(db.Boolean, nullable=False, server_default=str(False))
    paid = db.Column(db.SmallInteger, nullable=False, server_default=str(0))

    def __repr__(self) -> str:
        return f"<Bought Object>"

class PriceChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True, server_default=str(date(2021, 12, 1)))
    price = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Price_Change {self.item} ({self.date})>"

class AmountChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True, server_default=str(date(2021, 12, 1)))
    amount = db.Column(db.SmallInteger, nullable=False, server_default=str(1))
    
    def __repr__(self) -> str:
        return f"<Amount_Change {self.item} ({self.date})>"

class Receipt(db.Model):
    id = db.Column(db.Numeric(precision=22, scale=0), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    registered = db.Column(db.Boolean, nullable=False, server_default=str(False))
    paid = db.Column(db.SmallInteger, nullable=False, server_default=str(0))
    
    def __repr__(self) -> str:
        return f"<Receipt {self.id}>"

class ItemReceipt(db.Model):
    receipt = db.Column(db.ForeignKey("receipt.id"), primary_key=True)
    item = db.Column(db.ForeignKey("item.id"), primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<ItemReceipt {self.receipt}: {self.item}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))