from flask import abort, request, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import CheckItemsForm
from src import db, LOGGER
from models.receipt import Receipt
from models.login_token import LoginToken
from src.utils.pdf_receipt_parser import PDFReceipt
from src.utils.routes_utils import render_custom_template as render_template

PDFDir = "./"

@bp.route('/<int:receipt_id>', methods=['GET', 'POST'])
@login_required
def confirm_receipt_items(receipt_id: int):
    """Check items from a receipt if they should be accounted for payment.
    Get those items from the receipt PDF itself."""
    receipt_details = Receipt.query.get(receipt_id)
    if current_user.is_authenticated and current_user.id == receipt_details.LoginToken.Establishment.owner:
        receipt = PDFReceipt.getPDFReceiptFromFile(PDFDir + f"{receipt_details.id}.pdf")
        form = CheckItemsForm.new(receipt.items)
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
        for formitem in form.items:
            # print(formitem.new_brand.__dict__)
            print(formitem.data)
        if form.validate():
            print("valid")
        if form.validate_on_submit():
            return form.items.data
        return render_template("receipts/check_items.html", form=form)
    abort(403)