import jwt
from app import db, login
from datetime import date
from flask import current_app
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

item_category = db.Table("item_category",
    db.Column("item", db.ForeignKey("item.id"), primary_key=True, server_onupdate=db.FetchedValue()),
    db.Column("category", db.ForeignKey("category.id"), primary_key=True, server_onupdate=db.FetchedValue())
)

class User(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    LoginToken = db.relationship("LoginToken", backref='User', lazy='dynamic')
    Bought = db.relationship("Bought", secondary="login_token",
        lazy='dynamic', overlaps="User,LoginToken")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email})>"

class Establishment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    owner = db.Column(db.ForeignKey('user.id'), nullable=False)

    LoginToken = db.relationship("LoginToken", backref='Establishment', lazy='dynamic')
    Bought = db.relationship("Bought", secondary="login_token",
        lazy='dynamic', overlaps="Establishment,LoginToken,Bought")

    def __repr__(self) -> str:
        return f"<Establishment {self.id} ({self.name})>"

class LoginToken(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True, server_onupdate=db.FetchedValue())
    establishment = db.Column(db.ForeignKey('establishment.id'), primary_key=True, server_onupdate=db.FetchedValue())
    token = db.Column(db.String(15), nullable=False, unique=True)
    paid = db.Column(db.BigInteger, nullable=False, server_default=str(0))

    Receipt = db.relationship("Receipt", backref='LoginToken', lazy='dynamic')

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
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.ForeignKey('brand.id'), nullable=False, server_onupdate=db.FetchedValue())
    description = db.Column(db.Text, nullable=False)

    Category = db.relationship("Category", secondary=item_category, lazy="dynamic", back_populates="Item")
    Bought = db.relationship("Bought", backref='Item', lazy='dynamic')
    PriceChange = db.relationship("PriceChange", backref='Item', lazy='dynamic')
    AmountChange = db.relationship("AmountChange", backref='Item', lazy='dynamic')
    
    def __repr__(self) -> str:
        return f"<Item {self.id} ({self.name})>"

class Bought(db.Model):
    token = db.Column(db.ForeignKey('login_token.token'), primary_key=True, server_onupdate=db.FetchedValue())
    item = db.Column(db.ForeignKey('item.id'), primary_key=True, server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    registered = db.Column(db.Boolean, nullable=False, server_default=str(False))

    def __repr__(self) -> str:
        return f"<Bought Object>"

class PriceChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True, server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True, server_default=str(date(2021, 12, 1)))
    price = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Price_Change {self.item} ({self.date})>"

class AmountChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True, server_onupdate=db.FetchedValue())
    date = db.Column(db.Date, primary_key=True, server_default=str(date(2021, 12, 1)))
    amount = db.Column(db.SmallInteger, nullable=False, server_default=str(1))
    
    def __repr__(self) -> str:
        return f"<Amount_Change {self.item} ({self.date})>"

class Receipt(db.Model):
    id = db.Column(db.Numeric(precision=24, scale=0), primary_key=True, autoincrement=False)
    date = db.Column(db.Date, nullable=False)
    from_user = db.Column(db.ForeignKey("login_token.token"), server_onupdate=db.FetchedValue())
    registered = db.Column(db.Boolean, nullable=False, server_default=str(False))

    ItemReceipt = db.relationship("ItemReceipt", backref='Receipt', lazy='dynamic')
    
    def __repr__(self) -> str:
        return f"<Receipt {self.id}>"

class ItemReceipt(db.Model):
    receipt = db.Column(db.ForeignKey("receipt.id"), primary_key=True, server_onupdate=db.FetchedValue())
    item = db.Column(db.ForeignKey("item.id"), primary_key=True, server_onupdate=db.FetchedValue())
    amount = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<ItemReceipt {self.receipt}: {self.item}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))