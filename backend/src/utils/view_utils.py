from sqlalchemy_utils import create_view
from src import db, LOGGER
from src.models.amount_change import AmountChange
from src.models.bought import Bought
from src.models.price_change import PriceChange

def group_results(results: tuple) -> list:
    result_list = []
    LOGGER.debug("Grouping...")
    for result in results:
        try:
            result_user_index = [result[1] == result_item['email'] for result_item in result_list].index(True)
        except ValueError as e:
            result_list.append({"id": result[0], "email": result[1], "sum": 0, "item_infos": []})
            result_user_index = -1
        result_user = result_list[result_user_index]
        try:
            result_date_index = [result[2] == result_list_date['date'] for result_list_date in result_user["item_infos"]].index(True)
        except ValueError as e:
            result_user["item_infos"].append({'date': result[2], 'item_list': []})
            result_date_index = -1
        result_date = result_user['item_infos'][result_date_index]
        result_date['item_list'].append({'id': result[3], 'name': result[4], 'amount': result[5], 'price': result[6]})
    for result_user in result_list:
        if result_user.get('id'):
            for result_date in result_user['item_infos']:
                for result_item in result_date['item_list']:
                    result_user['sum'] += result_item['amount'] * result_item['price']
    LOGGER.debug("Grouped.")
    return result_list

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