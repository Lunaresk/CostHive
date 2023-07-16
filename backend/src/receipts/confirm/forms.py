from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CheckItemsForm(FlaskForm):
    items = MultiCheckboxField("Items")
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

    #TODO create new() method which loads the form for a specific receipt
    @classmethod
    def new(cls, itemArray):
        """
        """
        form = cls()
        return form