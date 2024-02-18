from src import LOGGER
from datetime import date as dtdate, timedelta
from flask_login import current_user
from models import Establishment, Item, LoginToken, User, Payment, Receipt, ReceiptItem
from src import db, LOGGER
from src.utils.view_utils import bought_with_prices as bwp

def group_results(results: tuple) -> list:
    """Grouping results as following:
    [
      {
        id: <usertoken>,
        email: <usermail>,
        sum: <sum of itemamounts*itemprices>,
        membership_dates: [
          (datetime.date(entry_date), datetime.date(exit_date))
        ],
        payments: [
          {
            date: datetime.date(payment date),
            amount: <payment (ct)>
          }
        ]
        item_infos: [
          {
            date: datetime.date(items date),
            item_list: [
              {
                id: <itemid>,
                name: <itemname>,
                amount: <itemamount>,
                price: <itemprice (ct)>
              }
            ]
          }
        ]
      }
    ]
    """
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
    # for result_user in result_list:
    #     if result_user.get('id'):
    #         for result_date in result_user['item_infos']:
    #             for result_item in result_date['item_list']:
    #                 result_user['sum'] += result_item['amount'] * result_item['price']
    LOGGER.debug("Grouped.")
    return result_list

def get_token_modifier_on_date(login_token_dates):
    # dict_people_modifier:
    # {datetime.date(x,y,z): {
    #  'add': <list of usertokens>,
    #  'remove: <list of usertokens>
    #  }
    # }
    dict_people_modifier = {}
    for tokendate in login_token_dates:
        if not tokendate.activation_date in dict_people_modifier:
            dict_people_modifier[tokendate.activation_date] = {}
        if not "add" in dict_people_modifier[tokendate.activation_date]:
            dict_people_modifier[tokendate.activation_date]['add'] = []
        dict_people_modifier[tokendate.activation_date]["add"].append(tokendate.token)
        if tokendate.deactivation_date != None:
            if not tokendate.deactivation_date in dict_people_modifier:
                dict_people_modifier[tokendate.deactivation_date] = {}
            if not "remove" in dict_people_modifier[tokendate.deactivation_date]:
                dict_people_modifier[tokendate.deactivation_date]['remove'] = []
            dict_people_modifier[tokendate.deactivation_date]["remove"].append(tokendate.token)
    return dict_people_modifier

def generate_better_list(dict_people_modifier):
    list_people_amount_per_date = [{"date": key, "people": value} for key, value in dict_people_modifier.items()]
    list_people_amount_per_date.sort(key=lambda x: x.get('date'))
    list_people_per_date = []
    LOGGER.debug("Preparing list")
    for i in range(len(list_people_amount_per_date)):
        list_people_per_date.append({'date': list_people_amount_per_date[i].get('date'), 'sum': 0})
        if i == 0:
            list_people_per_date[-1]['people'] = list_people_amount_per_date[i].get('people').get('add').copy()
        else:
            list_people_per_date[-1]['people'] = list_people_per_date[-2].get('people').copy()
            if 'add' in list_people_amount_per_date[i].get('people'):
                list_people_per_date[-1]['people'].extend(list_people_amount_per_date[i].get('people').get('add'))
            if 'remove' in list_people_amount_per_date[i].get('people'):
                for person in list_people_amount_per_date[i].get('people').get('remove'):
                    try:
                        list_people_per_date[-1]['people'].remove(person)
                    except ValueError as e:
                        LOGGER.debug(f'{person} not in list.')
    return list_people_per_date

def sum_entries(grouped_result_list, login_token_dates):
    dict_people_modifier = get_token_modifier_on_date(login_token_dates)
    LOGGER.debug(dict_people_modifier)
    LOGGER.debug("Preparing dict")
    list_people_per_date = generate_better_list(dict_people_modifier)
    LOGGER.debug("This is line 106")
    for result_user in grouped_result_list:
        relevant_date_index = 0
        for result_date in result_user['item_infos']:
            # TODO get relevant date index
            if not result_date.get('date'):
                result_date['item_list'] = []
                continue
            for i in range(relevant_date_index + 1, len(list_people_per_date)):
                if list_people_per_date[i].get('date') > result_date.get('date'):
                    # LOGGER.debug(f"{list_people_per_date[i].get('date')} > {result_date.get('date')}")
                    relevant_date_index = i-1
                    break
                if i == len(list_people_per_date)-1:
                    if list_people_per_date[i].get('date') <= result_date.get('date'):
                        relevant_date_index=i
            # LOGGER.debug(f"Relevant Date: {list_people_per_date[relevant_date_index].get('date')}, Index: {relevant_date_index}")
            # LOGGER.debug(f"Result Date: {result_date.get('date')}")
            for result_item in result_date['item_list']:
                result_user['sum'] += result_item['amount'] * result_item['price']
                list_people_per_date[relevant_date_index]['sum'] += result_item['amount'] * result_item['price']
    LOGGER.debug(list_people_per_date)
    for entry_people_per_date in list_people_per_date:
        for result_user in grouped_result_list:
            if result_user.get('id') in entry_people_per_date.get('people'):
                LOGGER.debug(f"Reducing sum of {result_user.get('id')} by {entry_people_per_date.get('sum')/len(entry_people_per_date.get('people'))}")
                result_user['sum'] -= entry_people_per_date.get('sum')/len(entry_people_per_date.get('people'))

def calculate_payments(grouped_result_list):
    LOGGER.debug("Calculating Payments")
    for result_user in grouped_result_list:
        payments:list[Payment] = Payment.query.filter_by(token=result_user.get('id')).order_by(Payment.date).all()
        if payments:
            LOGGER.debug(f"Payments found for user {result_user.get('id')}")
            result_user['payments'] = [{"date": x.date, "amount": x.amount} for x in payments]
            paymentsum = sum([x.amount for x in payments])
            LOGGER.debug(f"Adding payments of a total of {paymentsum} to {result_user.get('id')}")
            result_user['sum'] -= sum([x.amount for x in payments])

def get_report(**kwargs):
    query_select_boughts = db.session.query(
        LoginToken.token, User.email, bwp.c.date, bwp.c.item, Item.name, bwp.c.amount, bwp.c.price)
    query_select_boughts = query_select_boughts.select_from(LoginToken).join(User, LoginToken.user == User.id).join(
        bwp, LoginToken.token == bwp.c.token, isouter = True).join(Item, Item.id == bwp.c.item, isouter = True)
    query_select_receipts = db.session.query(
        Receipt.from_user, User.email, Receipt.date, ReceiptItem.item, ReceiptItem.name, ReceiptItem.amount, -ReceiptItem.price)
    query_select_receipts = query_select_receipts.select_from(User).join(LoginToken, LoginToken.user == User.id).join(
        Receipt, LoginToken.token == Receipt.from_user).join(ReceiptItem, ReceiptItem.receipt == Receipt.id)
    match kwargs:
        case {"token": token}:
            LOGGER.debug("Token present")
            query_select_boughts = query_select_boughts.filter_by(token = token)
            query_select_receipts = query_select_receipts.filter_by(token = token)
        case {"establishment": establishment}:
            LOGGER.debug("Establishment present")
            query_select_boughts = query_select_boughts.filter(LoginToken.establishment == establishment)
            query_select_receipts = query_select_receipts.filter(LoginToken.establishment == establishment)
            if current_user.id != Establishment.query.get(int(establishment)).owner:
                query_select_boughts = query_select_boughts.filter(User.id == current_user.id)
                query_select_receipts = query_select_receipts.filter(User.id == current_user.id)
            # if current_user.id == Establishment.query.get(int(establishment)).owner:
            #     _filter = db.session.query(LoginToken.token).filter_by(
            #         establishment=int(establishment))
            # else:
            #     _filter = db.session.query(LoginToken.token).filter_by(
            #         establishment=int(establishment), user=current_user.id)
            # query_select = query_select.filter(bwp.c.token.in_(_filter))
            # LOGGER.debug(str(query_select))
    match kwargs:
        case {"month": month}:
            LOGGER.debug("Month present")
            year = kwargs["year"] if "year" in kwargs else dtdate.today().year
            query_select_boughts = query_select_boughts.filter(bwp.c.date.between(dtdate(int(year), int(
                month), 1), dtdate(int(year), int(month)+1, 1)-timedelta(days=1)))
        case {"year": year}:
            LOGGER.debug("Year present")
            query_select_boughts = query_select_boughts.filter(bwp.c.date.between(
                dtdate(int(year), 1, 1), dtdate(int(year), 12, 31)))
    query_select = query_select_boughts.union(query_select_receipts)
    query_select = query_select.order_by(LoginToken.token, bwp.c.date, bwp.c.item)
    LOGGER.debug(str(query_select))
    results = query_select.all()
    return tuple(results)