from datetime import date
from models import AmountChange, Item, PriceChange, Receipt, ReceiptItem
from src import db, LOGGER

def insert_new_item(formitemdict: dict[str: str]):
    LOGGER.debug("Inserting new Item")
    newitem = Item(id=formitemdict.get('new_ean'), name=formitemdict.get('itemname'), description=formitemdict.get('new_description'), Brand=formitemdict.get('new_brand'))
    newamount = formitemdict.get('new_amount')
    if(newamount and newamount not in [0, 1]):
        newitem.AmountChange.append(AmountChange(amount=newamount))
    newprice = int(formitemdict.get("price").replace(",", ""))
    newitem.PriceChange.append(PriceChange(price=newprice))
    db.session.add(newitem)
    db.session.commit()


def insert_existing_item(formitemdict: dict[str: str], receipt_date: date = None):
    if not receipt_date:
        receipt_date = date.today()
    LOGGER.debug("Updating existing Item")
    itemobject: Item = formitemdict.get("existing_item")
    LOGGER.debug("Retrieving and comparing old and new price")
    # TODO compare the dates around the receipt date (before and after receipt date)
    pricechange_list: list[PriceChange] = itemobject.PriceChange.order_by(PriceChange.date.desc()).all()
    neighboring_prices: list[PriceChange] = get_neighboring_prices(pricechange_list, receipt_date)
    newprice = int(formitemdict.get("price").replace(",", ""))
    LOGGER.debug(neighboring_prices)
    if newprice != neighboring_prices[1].price:
        LOGGER.debug("New Price different from earlier price, inserting new price")
        new_pricechange = PriceChange(Item=itemobject, date=str(receipt_date), price=newprice)
        db.session.add(new_pricechange)
        if newprice == neighboring_prices[0].price:
            LOGGER.debug("New Price same as later price, removing later entry")
            db.session.delete(neighboring_prices[0])
        db.session.commit()

def insert_item_to_receipt(receipt: Receipt, item_dict: dict[str: str], item_index:int=0):
    receipt.ReceiptItem.append(ReceiptItem(item=item_index, amount=item_dict.get('amount'), price=int(item_dict.get('price').replace(',',''))))
    db.session.add(receipt)
    db.session.commit()

def clear_receipt_items(receipt: Receipt):
    receipt.registered = False
    for receipt_item in receipt.ReceiptItem.all():
        db.session.delete(receipt_item)
    db.session.commit()

def get_neighboring_prices(pricechange_list: list[PriceChange], target_date: date):
    upper_date, lower_date = None, None
    for pricechange in pricechange_list:
        if pricechange.date > target_date:
            if (not upper_date) or (upper_date.date > pricechange.date):
                upper_date = pricechange
        elif pricechange.date < target_date:
            if (not lower_date) or (lower_date.date < pricechange.date):
                lower_date = pricechange
    return [upper_date, lower_date]