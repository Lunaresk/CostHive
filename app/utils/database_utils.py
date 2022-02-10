from calendar import month
from app import db, LOGGER
from app.models import Bought, bought_with_prices
from copy import deepcopy
from datetime import date as dtdate, timedelta
from psycopg2 import errors
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

def insert_bought_items(user: str, items: dict, date: str = None):
    if not date:
        date = dtdate.today()
    for item, amount in deepcopy(items).items():
        query_insert = insert(Bought).values(user=user, item=int(item), date=date, amount=int(amount))
        query_insert = query_insert.on_conflict_do_update("bought_pkey", set_=dict(amount=text(f'bought.amount + {amount}')))
        try:
            db.session.execute(query_insert)
            db.session.commit()
        except errors.ForeignKeyViolation as e:
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            LOGGER.exception()
        else:
            del(items[item])
    return {'user':user, 'date': date, 'items': items} if items else {}

def get_report(**kwargs):
    query_select = bought_with_prices.select()
    if "user" in kwargs:
        query_select = query_select.where(bought_with_prices.c.user == kwargs['user'])
    match kwargs:
        case {"month": month}:
            year = kwargs["year"] if "year" in kwargs else dtdate.today().year
            query_select = query_select.where(bought_with_prices.c.date.between(dtdate(int(year), int(month), 1), dtdate(int(year), int(month)+1, 1)-timedelta(days=1)))
        case {"year": year}:
            query_select = query_select.where(bought_with_prices.c.date.between(dtdate(int(year), 1, 1), dtdate(int(year), 12, 31)))
    results = db.session.execute(query_select)
    return tuple(results)