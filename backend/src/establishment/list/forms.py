from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class JoinEstablishmentForm(FlaskForm):
    id = HiddenField("X")
    submit = SubmitField("Anfragen")
