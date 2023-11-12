from flask import abort, redirect, request, url_for
from flask_login import current_user, login_required
from os import rename
from werkzeug.utils import secure_filename
from . import bp
from .forms import UploadReceiptForm
from src import db, LOGGER
from models.receipt import Receipt
from models.login_token import LoginToken
from src.utils.pdf_receipt_parser import PDFReceipt
from src.utils.routes_utils import render_custom_template as render_template

PDFDir = "./"
@bp.route('/<int:establishment>', methods=['GET', 'POST'])
@login_required
def upload_receipt(establishment: int):
    """Upload of a receipt."""
    if current_user.is_anonymous:
        abort(403)
    if LoginToken.query.filter_by(establishment=establishment, user=current_user.id).first():
        form = UploadReceiptForm()
        LOGGER.debug(form.pdfReceipt.data)
        if form.validate_on_submit():
            pdfReceipt = form.pdfReceipt.data
            pdfReceipt.save(f"{PDFDir}/temp.pdf")
            with open(f"{PDFDir}/temp.pdf") as doc:
                receipt = PDFReceipt(doc)
            dbReceipt = Receipt(bonid = receipt.id, date = receipt.date,
                from_user = LoginToken.query.filter_by(establishment=establishment, user=current_user.id).first().token)
            db.session.add(dbReceipt)
            db.session.commit()
            rename(f"{PDFDir}/temp.pdf", f"{PDFDir}{secure_filename(f'{dbReceipt.id}.pdf')}")
            LOGGER.debug(receipt.text)
            return redirect(url_for("receipts.check_items.confirm_receipt_items", receipt_id = dbReceipt.id))
        else:
            LOGGER.debug(form.errors)
        return render_template("receipts/upload.html", form = form)
    abort(403)