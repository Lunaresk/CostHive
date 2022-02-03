from app.models import Brand, Category
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, DateField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NewItemForm(FlaskForm):
    id = IntegerField("Product EAN", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    date = DateField("Insert Date", validators=[DataRequired()])
    price_change = FloatField("Price", validators=[DataRequired()])
    amount_change = IntegerField("Amount", validators=[DataRequired()])
    category = SelectMultipleField("Categories", choices=[(c.id, c.name) for c in Category.query.order_by("name").all()], validators=[DataRequired()])
    brand = SelectField("Brand", choices=[(b.id, b.name) for b in Brand.query.order_by("name").all()], validators=[DataRequired()])
    submit = SubmitField("Submit")

class NewCategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class NewBrandForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")