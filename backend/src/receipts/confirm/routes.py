from flask import abort, request, url_for
from flask_login import current_user, login_required
from . import bp
from .forms import CheckItemsForm, UploadReceiptForm
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
    if "receipt" in request.args:
        receipt_details = Receipt.query.get(request.args['receipt'])
        if current_user.is_anonymous and current_user.id == receipt_details.LoginToken.Establishment.owner:
            receipt = PDFReceipt._getPDFReceiptFromFile(PDFDir + f"{receipt.date}_{receipt.id}.pdf")
            form = CheckItemsForm()
            # TODO: Precheck if items are already in database. If yes, check if item is present only once or multiple
            #       times and provide dropdown menu if necessary. If not, provide input field.
            temp_choices = []
            for item in receipt.items:
                match item:
                    case {"itemname": itemname, "price": price}:
                        temp_choices.append((itemname.replace(" ", "_"), f"{itemname, price}"))
                    case {"itemname": itemname, "price": price, "amount": amount}:
                        temp_choices.append((itemname.replace(" ", "_"), f"{itemname}, {price} * {amount}"))
            form.choices = temp_choices
            if form.validate_on_submit():
                pass # TODO
            return render_template("receipts/confirm_items.html")
    abort(403)