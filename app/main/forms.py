from app.models import Brand, Category
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class NewItemForm(FlaskForm):
    id = IntegerField("Product EAN", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    date = DateField("Insert Date", validators=[DataRequired()])
    price_change = FloatField("Price", validators=[DataRequired()])
    amount_change = IntegerField("Amount", validators=[Optional()])
    category = SelectMultipleField("Categories", choices=[], validators=[Optional()])
    brand = SelectField("Brand", choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")

    @classmethod
    def new(cls):
        form = cls()
        form.category.choices = [(c.id, c.name) for c in Category.query.order_by("name").all()]
        form.brand.choices = [(b.id, b.name) for b in Brand.query.order_by("name").all()]
        return form

class NewCategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

class NewBrandForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

class NewEstablishmentForm(FlaskForm):
    establishment_name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

class JoinEstablishmentForm(FlaskForm):
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})