from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import DateField, SelectField, SubmitField
from models import Establishment

class UploadReceiptForm(FlaskForm):
    user = SelectField("User", choices=[], render_kw={"class": "form-control"})
    date = DateField("Insert Date", render_kw={"class": "form-control"})
    pdfReceipt = FileField("PDF", validators=[FileAllowed(["pdf"], "Invalid Format, must be .pdf")])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

    @classmethod
    def new(cls, establishment):
        form = cls()
        form.user.choices = [(None, "")]+[(t.token, t.User.email) for t in Establishment.query.get(establishment).LoginToken.order_by("user").all()]
        return form