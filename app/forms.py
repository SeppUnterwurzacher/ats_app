from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class KPEinsatzUebung(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    druckl = IntegerField('Druck Links', validators=[DataRequired(), NumberRange(min=180)])
    druckr = IntegerField('Druck Rechts', validators=[DataRequired(), NumberRange(min=180)])
    submit = SubmitField('Fertig!')

class WartNeuGeraet(FlaskForm):
    bezeichnung = StringField('Bezeichnung:', validators=[DataRequired()])
    typ = StringField('Typ des Geräts:', validators=[DataRequired()])
    anschaffung = IntegerField('Jahr der Anschaffung:', validators=[DataRequired()])
    submit = SubmitField('Eintragen')