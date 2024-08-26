from datetime import date
from flask import abort, current_app, request, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import CheckCustomItemsEntryForm, CheckItemsEntryForm, CheckItemsForm, get_choices
from .utils import insert_existing_item, insert_new_item, insert_item_to_receipt, clear_receipt_items
from src import db, LOGGER
from models import AmountChange, Item, LoginToken, PriceChange, Receipt, ReceiptItem
from src.utils.modules.receipt_parser.pdf_receipt_parser import PDFReceipt
from src.utils.routes_utils import render_custom_template as render_template


@bp.route('/<int:receipt_id>', methods=['GET', 'POST'])
@login_required
def confirm_receipt_items(receipt_id: int):
    """Check items from a receipt if they should be accounted for payment.
    Get those items from the receipt PDF itself."""
    PDFDir: str = current_app.config["RECEIPT_FOLDER"]
    receipt_details: Receipt = Receipt.query.get(receipt_id)
    if current_user.is_authenticated and current_user.id == receipt_details.LoginToken.Establishment.owner:
        receipt: PDFReceipt = PDFReceipt.getPDFReceiptFromFile(PDFDir + f"/{receipt_details.id}.pdf")
        form: CheckItemsForm = CheckItemsForm.new(receipt.items)
        _template = CheckCustomItemsEntryForm(prefix="custom_items-_-")
        # TODO: Precheck if items are already in database. If yes, check if item is present only once or multiple
        #       times and provide dropdown menu if necessary. If not, provide input field.
        # temp_choices = []
        # for item in receipt.items:
        #     match item:
        #         case {"itemname": itemname, "price": price}:
        #             temp_choices.append((itemname.replace(" ", "_"), f"{itemname, price}"))
        #         case {"itemname": itemname, "price": price, "amount": amount}:
        #             temp_choices.append((itemname.replace(" ", "_"), f"{itemname}, {price} * {amount}"))
        # form.choices = temp_choices
        # print(form.data)
        # for formitem in form.items:
        #     LOGGER.debug(formitem.data)
        if form.validate():
            LOGGER.debug("valid")
        else:
            LOGGER.debug(form.errors)
        if form.validate_on_submit():
            LOGGER.debug("Validate on submit")
            clear_receipt_items(receipt=receipt_details)
            for itempos, formitem in enumerate(form.items):
                LOGGER.debug("Iterating through form items")
                formitemdata = formitem.data
                if formitemdata.get('requesting'):
                    LOGGER.debug("Item requested")
                    LOGGER.debug(formitemdata)
                    insert_item_to_receipt(receipt=receipt_details, item_dict=receipt.items[itempos], item_index=itempos)
                    if formitemdata.get('new_or_existing') == get_choices()[0][0]: # New Item
                        LOGGER.debug("New Item catched")
                        insert_new_item(formitemdict=formitemdata)
                    elif formitemdata.get('new_or_existing') == get_choices()[1][0]: # Existing Item
                        LOGGER.debug("Existing Item catched")
                        insert_existing_item(formitemdict=formitemdata, receipt_date=receipt.date)
                    elif formitemdata.get('new_or_existing') == get_choices()[2][0]: # Item not for DB
                        LOGGER.debug("Not listed Item catched")
                    else:
                        LOGGER.debug("Cold catched")
                        abort(400)
            for itempos, formcustomitem in enumerate(form.custom_items):
                formcustomitemdata = formcustomitem.data
                custom_item_dict = {}
                custom_item_dict['amount'] = formcustomitemdata.get('amount', 1)
                custom_item_dict['price'] = formcustomitemdata.get('price')
                custom_item_dict['itemname'] = formcustomitemdata.get('itemname')
                LOGGER.debug(formcustomitem)
                LOGGER.debug(custom_item_dict)
                insert_item_to_receipt(receipt=receipt_details, item_dict=custom_item_dict, item_index=len(form.items)+itempos)
                LOGGER.debug("Iterating through form custom items")
        return render_template("receipts/check_items.html", form=form, _template=_template)
    abort(403)