from copy import deepcopy
from datetime import date as dtdate, timedelta
from flask_login import current_user
from psycopg2 import errors
from random import choice as rndchoice
from sqlalchemy import and_, text
from sqlalchemy.dialects.postgresql import insert
from string import ascii_letters, digits
from .view_utils import bought_with_prices as bwp
from src import db, LOGGER
from models import Bought, BoughtWithUnknownItem, Establishment, Item, LoginToken, User


def insert_bought_items(token: str, dates: list[dict[str: any]]):
    for date in deepcopy(dates):
        date_index = dates.index(date)
        for item in deepcopy(date['items']):
            query_insert = insert(Bought).values(token=token, item=int(
                item['item_id']), date=date['date'], amount=int(item["amount"]))
            query_insert = query_insert.on_conflict_do_update(
                "bought_pkey", set_=dict(amount=text(f'bought.amount + {int(item["amount"])}')))
            if(_query_successful(query_insert)):
                item_index = dates[date_index]['items'].index(item)
                del (dates[date_index]['items'][item_index])
            else:
                query_insert = insert(BoughtWithUnknownItem).values(token=token, item=int(
                    item['item_id']), date=date['date'], amount=int(item["amount"]))
                query_insert = query_insert.on_conflict_do_update(
                "bought_with_unknown_item_pkey", set_=dict(amount=text(f'bought_with_unknown_item.amount + {int(item["amount"])}')))
                if(_query_successful(query_insert)):
                    item_index = dates[date_index]['items'].index(item)
                    del (dates[date_index]['items'][item_index])
        if len(dates[date_index]['items']) == 0:
            del (dates[date_index])
    return {'token': token, 'dates': dates} if dates else {}

def _query_successful(query):
    try:
        db.session.execute(query)
        db.session.commit()
    except errors.ForeignKeyViolation as e:
        db.session.rollback()
        return False
    except Exception as e:
        db.session.rollback()
        LOGGER.exception("")
        return False
    else:
        return True

def generate_token(length=15, allowed_chars=ascii_letters + digits):
    new_token = "".join((rndchoice(allowed_chars) for i in range(length)))
    if not LoginToken.query.filter_by(token=new_token).first():
        return new_token
    return generate_token()
