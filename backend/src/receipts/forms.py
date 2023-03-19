from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import BooleanField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import Optional

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class UploadReceiptForm(FlaskForm):
    pdfReceipt = FileField("PDF", validators=[FileRequired(), FileAllowed(["pdf"], "Invalid Format, must be .pdf")])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-3"})

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