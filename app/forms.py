from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
from datetime import date


class KPEinsatzUebung(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    traeger = StringField('Name')
    druckl = IntegerField('Druck Links', validators=[DataRequired(), NumberRange(min=180)])
    druckr = IntegerField('Druck Rechts', validators=[DataRequired(), NumberRange(min=180)])
    submit = SubmitField('Fertig!')

class WartNeuGeraet(FlaskForm):
    bezeichnung = StringField('Bezeichnung:', validators=[DataRequired()])
    typ = StringField('Typ des Geräts:', validators=[DataRequired()])
    anschaffung = IntegerField('Jahr der Anschaffung:', validators=[DataRequired(), NumberRange(min=1000, max=date.today().year)])
    submit = SubmitField('Eintragen')

class LogbuchAuswahl(FlaskForm):
    geraet = SelectField('Gerät auswählen', choices=[(1, 'Gerät 1'), (2, 'Gerät 2')], validators=[DataRequired()])
    year = SelectField('Jahr', validators=[DataRequired()])
    submit = SubmitField('Laden')