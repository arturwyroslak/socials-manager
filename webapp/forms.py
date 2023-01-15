from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    BooleanField,
    RadioField
)
from wtforms.validators import InputRequired, Length

class LinkedInPost(FlaskForm):

    content = StringField(
        "content",
        validators=[
            InputRequired()
        ],
        render_kw={"placeholder": "Content"}
    )