from sqlalchemy_utils import create_view
from src import db, LOGGER
from models.amount_change import AmountChange
from models.bought import Bought
from models.price_change import PriceChange

def selectable_price_per_amount_view():
    p = db.aliased(PriceChange, name="p")
    a = db.aliased(AmountChange, name="a")
    date = db.func.greatest(p.date, a.date).label("date")
    price = db.func.ceil(p.price.cast(db.Float)/db.func.coalesce(a.amount, 1)).label("price")
    select = db.select(p.item.label("item"), date, price)
    select = select.distinct(p.item, date)
    select = select.join(a, p.item==a.item, isouter=True)
    select = select.order_by(p.item, db.desc(db.func.greatest(p.date, a.date)))
    return select

price_per_amount = create_view("price_per_amount", selectable_price_per_amount_view(), db.metadata)

def selectable_bought_with_prices_view():
    b = db.aliased(Bought, name="b")
    ppa = price_per_amount.alias("ppa")
    select = db.select(b.token.label("token"), b.date.label("date"), b.item.label("item"), b.amount.label("amount"), ppa.c.price.label("price"))
    select = select.distinct(b.token, b.date, b.item)
    select = select.join(ppa, b.item==ppa.c.item)
    select = select.where(ppa.c.date<=b.date)
    select = select.order_by(db.desc(b.token), db.desc(b.date), db.desc(b.item), db.desc(ppa.c.date))
    return select

bought_with_prices = create_view("bought_with_prices", selectable_bought_with_prices_view(), db.metadata)