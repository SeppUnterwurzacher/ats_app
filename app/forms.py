import imp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class PrueferForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('weiter')

class DruckForm(FlaskForm):
    druckl = IntegerField('Druck Links', validators=[DataRequired(), NumberRange(min=180)])
    druckr = IntegerField('Druck Rechts', validators=[DataRequired(), NumberRange(min=180)])
    submit = SubmitField('weiter')