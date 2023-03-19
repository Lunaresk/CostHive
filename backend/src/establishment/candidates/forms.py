from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class EvaluateCandidateForm(FlaskForm):
    candidate_id = HiddenField("X")
    accept = SubmitField("Akzeptieren", render_kw={"class": "btn btn-success mt-3"})
    deny = SubmitField("Ablehnen", render_kw={"class": "btn btn-danger mt-3"})