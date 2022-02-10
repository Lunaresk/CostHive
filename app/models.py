from app import db, login
from flask_login import UserMixin
from sqlalchemy.sql import text
from sqlalchemy_utils.view import create_view
from werkzeug.security import generate_password_hash, check_password_hash

item_category = db.Table("item_category",
    db.Column("item", db.ForeignKey("item.id"), primary_key=True),
    db.Column("category", db.ForeignKey("category.id"), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    Bought = db.relationship("Bought", backref='User', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.name})>"

class LoginToken(db.Model):
    user = db.Column(db.ForeignKey('user.id'), primary_key=True)
    token = db.Column(db.String(32), nullable=False)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return f"<Brand {self.id} ({self.name})>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

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
    user = db.Column(db.ForeignKey('user.id'), primary_key=True)
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    # registered = db.Column(db.Boolean, nullable=False, default=False)
    # paid = db.Column(db.SmallInteger, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"<Bought Object>"

class PriceChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    price = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Price_Change {self.item} ({self.date})>"

class AmountChange(db.Model):
    item = db.Column(db.ForeignKey('item.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False, default=1)
    
    def __repr__(self) -> str:
        return f"<Amount_Change {self.item} ({self.date})>"

class Receipt(db.Model):
    id = db.Column(db.Numeric(precision=22, scale=0), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    registered = db.Column(db.Boolean, nullable=False, default=False)
    paid = db.Column(db.SmallInteger, nullable=False, default=0)
    
    def __repr__(self) -> str:
        return f"<Receipt {self.id}>"

class ItemReceipt(db.Model):
    receipt = db.Column(db.ForeignKey("receipt.id"), primary_key=True)
    item = db.Column(db.ForeignKey("item.id"), primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    
    def __repr__(self) -> str:
        return f"<ItemReceipt {self.receipt}: {self.item}>"

def query_price_per_amount_view():
    p = db.aliased(PriceChange, name="p")
    a = db.aliased(AmountChange, name="a")
    date = db.func.greatest(p.date, a.date).label("date")
    price = (db.func.ceil(p.price.cast(db.Float)/db.func.coalesce(a.amount, 1))/100).label("price")
    select = db.select(p.item.label("item"), date, price)
    select = select.distinct(p.item, date)
    select = select.join(a, p.item==a.item, isouter=True)
    select = select.order_by(p.item, db.desc(db.func.greatest(p.date, a.date)))
    return select

price_per_amount = create_view("price_per_amount", query_price_per_amount_view(), db.metadata)

def query_bought_with_prices_view():
    b = db.aliased(Bought, name="b")
    ppa = price_per_amount.alias("ppa")
    select = db.select(b.user.label("user"), b.date.label("date"), b.item.label("item"), b.amount.label("amount"), ppa.c.price.label("price"))
    select = select.distinct(b.user, b.date, b.item)
    select = select.join(ppa, b.item==ppa.c.item)
    select = select.where(ppa.c.date<=b.date)
    select = select.order_by(db.desc(b.user), db.desc(b.date), db.desc(b.item), db.desc(ppa.c.date))
    return select

bought_with_prices = create_view("bought_with_prices", query_bought_with_prices_view(), db.metadata)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))