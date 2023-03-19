from src.models.brand import Brand
from src.models.category import Category
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class NewItemForm(FlaskForm):
    id = IntegerField("Product EAN", validators=[DataRequired()], render_kw={"class": "form-control"})
    name = StringField("Name", validators=[DataRequired()], render_kw={"class": "form-control"})
    description = StringField("Description", validators=[DataRequired()], render_kw={"class": "form-control"})
    date = DateField("Insert Date", validators=[DataRequired()], render_kw={"class": "form-control"})
    price_change = FloatField("Price", validators=[DataRequired()], render_kw={"class": "form-control"})
    amount_change = IntegerField("Amount", validators=[Optional()], render_kw={"class": "form-control"})
    category = SelectMultipleField("Categories", choices=[], validators=[Optional()], render_kw={"class": "form-control"})
    brand = SelectField("Brand", choices=[], validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

    @classmethod
    def new(cls):
        form = cls()
        form.category.choices = [(c.id, c.name) for c in Category.query.order_by("name").all()]
        form.brand.choices = [(b.id, b.name) for b in Brand.query.order_by("name").all()]
        return form