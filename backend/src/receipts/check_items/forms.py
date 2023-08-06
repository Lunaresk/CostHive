from collections import namedtuple
from flask_wtf import FlaskForm
from models import Brand, Item
from src.utils.models.query_factories import all_brands, all_items
from wtforms import BooleanField, HiddenField, FieldList, Form, FormField, IntegerField, RadioField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField


class CheckItemsEntryForm(Form):
    # TODO Fertig machen x.x
    itemname = HiddenField('itemname', validators=[DataRequired()])
    price = HiddenField('price', validators=[DataRequired()])
    requesting = BooleanField("", default=False, render_kw={
                              "class": "form-check-input"})
    new_or_existing = RadioField("", choices=[
                                 (0, "New"), (1, "Existing")], render_kw={"class": "form-check-input", "style": "display:none"}, validate_choice=False)
    # Fields for new Item
    new_description = StringField("Description", render_kw={"class": "form-control"})
    new_amount_change = IntegerField("Amount", render_kw={"class": "form-control"})
    new_brand = QuerySelectField("Brand", query_factory=all_brands, render_kw={"class": "form-control"}, allow_blank=True)
    # Fields for existing Item
    existing_item = QuerySelectField("Item", query_factory=all_items, render_kw={"class": "form-control"}, allow_blank=True)

    def validate_new_or_existing(self, new_or_existing):
        if (self.requesting.data and not new_or_existing.data):
            raise ValidationError(
                "Please choose if it's a new or existing Item.")

    def validate_existing_item(self, existing_item):
        if (existing_item.data and self.new_or_existing.data == 0):
            raise ValidationError("You shouldn't be able to enter this.")

    def validate_new_description(self, new_description):
        if (new_description.data and self.new_or_existing.data == 1):
            raise ValidationError("You shouldn't be able to enter this.")

    def validate_new_amount_change(self, new_amount_change):
        if (new_amount_change.data and self.new_or_existing.data == 1):
            raise ValidationError("You shouldn't be able to enter this.")

    def validate_new_brand(self, new_brand):
        if (new_brand.data and self.new_or_existing.data == 1):
            raise ValidationError("You shouldn't be able to enter this.")


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
            check_items_entry.append(CheckItemsEntry(item['itemname'], item['price'], 0))
        check_items = CheckItems(check_items_entry)
        form = cls(obj=check_items)

        print(f"{form.items.entries}")
        return form
