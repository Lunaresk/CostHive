from app.models import Brand, Category, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, DateField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

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
    submit = SubmitField("Submit")

class NewBrandForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class NeueWGForm(FlaskForm):
    wg_name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class WGBeitretenForm(FlaskForm):
    submit = SubmitField("Submit")