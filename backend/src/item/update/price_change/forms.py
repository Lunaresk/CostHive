from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, FloatField, SubmitField
from wtforms.validators import DataRequired

class NewPriceChangeForm(FlaskForm):
    id = HiddenField("Product EAN", validators=[DataRequired()], render_kw={"class": "form-control"})
    date = DateField("Insert Date", validators=[DataRequired()], render_kw={"class": "form-control"})
    price_change = FloatField("Price", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})