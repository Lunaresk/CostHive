from collections import namedtuple
from flask_wtf import FlaskForm
from src.utils.models.query_factories import all_brands, all_items
from wtforms import BooleanField, HiddenField, FieldList, Form, FormField, IntegerField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField


def radio_validator(choice):
    field_names = ["New", "Existing"]

    def _radio_validator(form, field):
        if (form.new_or_existing.data == choice and (not field.data)):
            raise ValidationError(
                f"Field is required if you choose '{field_names[choice-1]}'.")
    return _radio_validator

def get_choices():
    return [(1, "New"), (2, "Existing"), (3, "Not listed")]

class CheckItemsEntryForm(Form):
    itemname = HiddenField('itemname', validators=[DataRequired()])
    price = HiddenField('price', validators=[DataRequired()])
    requesting = BooleanField("", default=False,
                              render_kw={"class": "form-check-input"})
    new_or_existing = RadioField("",
                                 choices=get_choices(),
                                 render_kw={"class": "form-check form-check-inline form-check-input"},
                                 coerce=int, default=3)
    # Fields for new Item
    new_ean = IntegerField("EAN ID", render_kw={
                           "class": "form-control"}, validators=[radio_validator(1)],
                           default=0)
    new_description = StringField("Description", render_kw={
                                  "class": "form-control"}, validators=[radio_validator(1)])
    new_amount_change = IntegerField("Amount",
                                     render_kw={"class": "form-control"},
                                     validators=[radio_validator(1)],
                                     default=0)
    new_brand = QuerySelectField("Brand", query_factory=all_brands,
                                 render_kw={"class": "form-control"},
                                 allow_blank=True, validators=[radio_validator(1)])
    # Fields for existing Item
    existing_item = QuerySelectField("Item", query_factory=all_items,
                                     render_kw={"class": "form-control"},
                                     allow_blank=True, validators=[radio_validator(2)])

    def validate_new_or_existing(self, new_or_existing):
        if (self.requesting.data and not new_or_existing.data):
            raise ValidationError(
                "Please choose if it's a new or existing Item.")


class CheckItemsForm(FlaskForm):
    items = FieldList(FormField(CheckItemsEntryForm))
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

    @classmethod
    def new(cls, itemarray):
        CheckItemsEntry = namedtuple(
            "CheckItemsEntry", ["itemname", "price", "new_brand"])
        CheckItems = namedtuple("CheckItems", ["items"])
        check_items_entry = []
        for item in itemarray:
            check_items_entry.append(CheckItemsEntry(
                item['itemname'], item['price'], 0))
        check_items = CheckItems(check_items_entry)
        form = cls(obj=check_items)

        print(f"{form.items.entries}")
        return form
