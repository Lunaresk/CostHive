from flask import abort, redirect, request, url_for
from flask_login import current_user, login_required
from os import rename
from werkzeug.utils import secure_filename
from . import bp
from .forms import UploadReceiptForm
from src import db, LOGGER
from models.receipt import Receipt
from models.login_token import LoginToken
from src.utils.modules.receipt_parser.pdf_receipt_parser import PDFReceipt
from src.utils.routes_utils import render_custom_template as render_template

PDFDir = "./"
@bp.route('/<int:establishment>', methods=['GET', 'POST'])
@login_required
def upload_receipt(establishment: int):
    """Upload of a receipt."""
    if current_user.is_anonymous:
        abort(403)
    if LoginToken.query.filter_by(establishment=establishment, user=current_user.id).first():
        form = UploadReceiptForm.new(establishment)
        LOGGER.debug(form.pdfReceipt.data)
        if form.validate_on_submit():
            pdfReceipt = form.pdfReceipt.data
            receipt_date = form.date.data
            bonid = None
            if form.user.data:
                from_user = form.user.data
            else:
                from_user = LoginToken.query.filter_by(establishment=establishment, user=current_user.id).first_or_404().token
            if pdfReceipt:
                pdfReceipt.save(f"{PDFDir}/temp.pdf")
                with open(f"{PDFDir}/temp.pdf") as doc:
                    receipt = PDFReceipt(doc)
                bonid = receipt.id
                if receipt.date:
                    receipt_date = receipt.date
            dbReceipt = Receipt(date = receipt_date, from_user = from_user, bonid = bonid)
            db.session.add(dbReceipt)
            db.session.commit()
            if pdfReceipt:
                rename(f"{PDFDir}/temp.pdf", f"{PDFDir}{secure_filename(f'{dbReceipt.id}.pdf')}")
                LOGGER.debug(receipt.words)
            return redirect(url_for("receipts.check_items.confirm_receipt_items", receipt_id = dbReceipt.id))
        else:
            LOGGER.debug(form.errors)
        return render_template("receipts/upload.html", form = form)
    abort(403)