from flask import abort, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from . import bp
from .forms import UploadReceiptForm
from src import db, LOGGER
from models.receipt import Receipt
from models.login_token import LoginToken
from src.utils.pdf_receipt_parser import PDFReceipt
from src.utils.routes_utils import render_custom_template as render_template

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
            if form.validate_on_submit():
                receipt = PDFReceipt(form.pdfReceipt.data)
                dbReceipt = Receipt(id = receipt.id, date = receipt.date,
                    from_user = LoginToken.query.filter_by(establishment=request.args['establishment'], user=current_user.id).first().token)
                form.pdfReceipt.data.save(PDFDir + secure_filename(f"{str(receipt.date)}_{receipt.id}.pdf"))
                db.session.add(dbReceipt)
                db.session.commit()
                return receipt.text.replace("\n", "<br>")
            else:
                LOGGER.debug(form.errors)
            return render_template("receipts/upload.html", form = form)
    abort(403)