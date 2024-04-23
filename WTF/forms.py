from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, URL, AnyOf, NumberRange

class AddPetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired(), AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')
