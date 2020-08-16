from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InTextForm(FlaskForm):
    inputtext = StringField(validators=[
        DataRequired(),
        Length(max=40),
        ]
        )
    submit = SubmitField("in_txt")

class InImageForm(FlaskForm):
    inputimage = FileField(validators=[FileRequired()])
    submit = SubmitField("in_img")
