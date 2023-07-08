from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class NewAmountChangeForm(FlaskForm):
    id = HiddenField("Product EAN", validators=[DataRequired()], render_kw={"class": "form-control"})
    date = DateField("Insert Date", validators=[DataRequired()], render_kw={"class": "form-control"})
    amount_change = IntegerField("Amount", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})