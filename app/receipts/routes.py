from app import db, LOGGER
from app.receipts import bp
from app.receipts.forms import CheckItemsForm, UploadReceiptForm
from app.models import Receipt, LoginToken
from app.utils.routes_utils import render_custom_template as render_template
from flask import abort, request, url_for
from flask_login import current_user, login_required
from app.utils.pdf_receipt_parser import PDFReceipt

PDFDir = "./"

@bp.route('/upload_receipt', methods=['GET', 'POST'])
@login_required
def upload_receipt():
    """Upload of a receipt."""
    if current_user.is_anonymous:
        abort(403)
    if "establishment" in request.args:
        if LoginToken.query.filter_by(establishment=request.args['establishment'], user=current_user.id).first():
            form = UploadReceiptForm()
            LOGGER.debug(form.pdfReceipt.data)
            if form.is_submitted():
                LOGGER.debug("submitted")
            if form.validate():
                LOGGER.debug("valid")
            else:
                LOGGER.debug(form.errors)
            if form.validate_on_submit():
                receipt = PDFReceipt(form.pdfReceipt.data)
                dbReceipt = Receipt(id = receipt.id, date = receipt.date,
                    from_user = LoginToken.query.filter_by(establishment=request.args['establishment'], user=current_user.id).first().token)
                form.pdfReceipt.data.save(PDFDir + f"{str(receipt.date)}_{receipt.id}.pdf")
                db.session.add(dbReceipt)
                db.session.commit()
                return receipt.text.replace("\n", "<br>")
            return render_template("receipts/upload.html", form = form)
    abort(403)

@bp.route('/confirm_receipt', methods=['GET', 'POST'])
@login_required
def confirm_receipt_items():
    """Check items from a receipt if they should be accounted for payment."""
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