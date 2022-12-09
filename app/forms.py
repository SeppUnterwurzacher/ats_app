from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from datetime import date


class KPEinsatzUebung(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    traeger = StringField('Name')
    druckl = IntegerField('Druck Links', validators=[DataRequired()])
    druckr = IntegerField('Druck Rechts')
    submit = SubmitField('Fertig!')

class WartNeuGeraet(FlaskForm):
    bezeichnung = StringField('Bezeichnung:', validators=[DataRequired()])
    typ = SelectField('Typ des Geräts:', choices=[('200bar', '200bar'), ('300bar', '300bar')], validators=[DataRequired()])
    anschaffung = IntegerField('Jahr der Anschaffung:', validators=[DataRequired(), NumberRange(min=1000, max=date.today().year)])
    info = TextAreaField('Zusatz Info',validators=[Optional()])
    pin = IntegerField('Pin festlegen/ändern', validators=[Optional(), NumberRange(min=1000, max=9999)])
    submit = SubmitField('Eintragen')

class LogbuchAuswahl(FlaskForm):
    geraet = SelectField('Gerät auswählen', choices=[(1, 'Gerät 1'), (2, 'Gerät 2')], validators=[DataRequired()])
    year = SelectField('Jahr', validators=[DataRequired()])
    submit = SubmitField('Laden')

class GeraeteLogin(FlaskForm):
    pin_geraet = PasswordField('Pin', validators=[DataRequired(), Length(4, 4)])
    submit = SubmitField('Laden')

class WartLogin(FlaskForm):
    email = EmailField('Benutzer', validators=[DataRequired()])
    pw = PasswordField('Passwort')
    submit = SubmitField('anmelden')

class WartQR(FlaskForm):
    geraet = SelectField('Gerät auswählen', choices=[(1, 'Gerät 1'), (2, 'Gerät 2')], validators=[DataRequired()])
    pin_geraet = PasswordField('Pin', validators=[DataRequired(), Length(4, 4)])
    submit = SubmitField('QR-Code erstellen')