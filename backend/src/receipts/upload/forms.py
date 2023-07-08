from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

class UploadReceiptForm(FlaskForm):
    pdfReceipt = FileField("PDF", validators=[FileRequired(), FileAllowed(["pdf"], "Invalid Format, must be .pdf")])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})