from app import db, LOGGER
from app.models import Bought, Establishment, Item, LoginToken, User
from app.utils.view_utils import bought_with_prices as bwp
from copy import deepcopy
from datetime import date as dtdate, timedelta
from flask_login import current_user
from psycopg2 import errors
from random import choice as rndchoice
from sqlalchemy import and_, text
from sqlalchemy.dialects.postgresql import insert
from string import ascii_letters, digits

def insert_bought_items(token: str, items: dict, date: str = None):
    if not date:
        date = dtdate.today()
    for item, amount in deepcopy(items).items():
        query_insert = insert(Bought).values(token=token, item=int(item), date=date, amount=int(amount))
        query_insert = query_insert.on_conflict_do_update("bought_pkey", set_=dict(amount=text(f'bought.amount + {amount}')))
        try:
            db.session.execute(query_insert)
            db.session.commit()
        except errors.ForeignKeyViolation as e:
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            LOGGER.exception("")
        else:
            del(items[item])
    return {'user':token, 'date': date, 'items': items} if items else {}

def get_report(**kwargs):
    query_select = db.session.query(bwp.c.token, User.username, bwp.c.date, bwp.c.item, Item.name, bwp.c.amount, bwp.c.price)
    query_select = query_select.select_from(bwp).join(LoginToken, LoginToken.token==bwp.c.token).join(User, LoginToken.user==User.id).join(Item, Item.id==bwp.c.item)
    match kwargs:
        case {"token": token}:
            LOGGER.debug("Token present")
            query_select = query_select.filter_by(token == token)
        case {"establishment": establishment}:
            LOGGER.debug("Establishment present")
            if current_user.id == Establishment.query.get(int(establishment)).owner:
                _filter = db.session.query(LoginToken.token).filter_by(establishment = int(establishment))
            else:
                _filter = db.session.query(LoginToken.token).filter_by(establishment = int(establishment), user=current_user.id)
            query_select = query_select.filter(bwp.c.token.in_(_filter))
            # LOGGER.debug(str(query_select))
    match kwargs:
        case {"month": month}:
            LOGGER.debug("Month present")
            year = kwargs["year"] if "year" in kwargs else dtdate.today().year
            query_select = query_select.filter(bwp.c.date.between(dtdate(int(year), int(month), 1), dtdate(int(year), int(month)+1, 1)-timedelta(days=1)))
        case {"year": year}:
            LOGGER.debug("Year present")
            query_select = query_select.filter(bwp.c.date.between(dtdate(int(year), 1, 1), dtdate(int(year), 12, 31)))
    query_select = query_select.order_by(bwp.c.token, bwp.c.date, bwp.c.item)
    # LOGGER.debug(str(query_select))
    results = query_select.all()
    return tuple(results)

def get_unregistered_and_register(intEstablishment: int):
    LOGGER.debug("Getting unregistered")
    establishment = Establishment.query.get(intEstablishment)
    if current_user.id != establishment.owner:
        LOGGER.debug("!!!Wrong User!!!")
        return False
    query_select = db.session.query(bwp.c.token, User.username, bwp.c.date, bwp.c.item, Item.name, bwp.c.amount, bwp.c.price)
    query_select = query_select.select_from(bwp).join(LoginToken, LoginToken.token==bwp.c.token).join(User, LoginToken.user==User.id)
    query_select = query_select.join(Item, Item.id==bwp.c.item).join(Bought, and_(Bought.token==bwp.c.token, Bought.item==bwp.c.item, Bought.date==bwp.c.date))
    query_select = query_select.filter(bwp.c.token.in_(db.session.query(LoginToken.token).filter_by(establishment = intEstablishment)))
    query_select = query_select.filter(Bought.registered == False)
    query_select = query_select.order_by(bwp.c.token, bwp.c.date, bwp.c.item)
    results = query_select.all()
    unregistered_boughts = establishment.Bought.filter_by(registered = False).all()
    for x in unregistered_boughts:
        x.registered = True
    db.session.commit()
    return results


def generate_token(length = 15, allowed_chars = ascii_letters + digits):
    new_token = "".join((rndchoice(allowed_chars) for i in range(length)))
    if not LoginToken.query.filter_by(token=new_token).first():
        return new_token
    return generate_token()