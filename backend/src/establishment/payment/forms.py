from models import LoginToken
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class NewPaymentForm(FlaskForm):
    token = SelectField("User", validators=[DataRequired()], render_kw={"class": "form-control"})
    date = DateField("Date", validators=[DataRequired()], render_kw={"class": "form-control"})
    amount = IntegerField("Amount (in ct)", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

    @classmethod
    def new(cls, establishment_id):
        form = cls()
        tokens_for_establishment = LoginToken.query.filter_by(establishment=int(establishment_id)).order_by("user").all()
        form.token.choices = [(t.token, t.User.email) for t in tokens_for_establishment]
        return form