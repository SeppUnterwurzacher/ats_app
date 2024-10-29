from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, Email, EqualTo, ValidationError
from datetime import date
from app.models import Geraete, Benutzer
from flask_login import current_user
from flask import session


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

    def validate_bezeichnung(self, bezeichnung):
        geraet = Geraete.query.filter_by(name_geraet=bezeichnung.data, id_feuerwehr=current_user.id).first()

        if geraet is not None:
            if geraet.id != session['geraet_id']:
                raise ValidationError('Diese Bezeichnung ist in deiner Feuerwehr schon vorhanden')

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

class EditFeuerwehr(FlaskForm):
    name = StringField('Name Feuerwehr', validators=[DataRequired()])
    strasse = StringField('Strasse mit Hausnummer', validators=[DataRequired()])
    plz = IntegerField('Plz', validators=[DataRequired(), NumberRange(min=1000, max=9999)])
    ort = StringField('Ort', validators=[DataRequired()])
    submit = SubmitField('speichern')

class EditBenutzer(FlaskForm):
    benutzer = StringField('Name', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[DataRequired(), Email()])
    submit_bn = SubmitField('speichern')

    # Prüfung auf doppelte Benutzernamen deaktiviert, da eindeutige Eigenschaft die E-Mail Adresse ist
    # def validate_benutzer(self, benutzer):
    #     user = Benutzer.query.filter_by(benutzer=benutzer.data).first()
    #     if user is not None:
    #         if user.id != session['benutzer_id']:
    #             raise ValidationError('Benutzername konnte nicht geändert werden, da bereits vergeben')
            
    def validate_email(self, email):
        user = Benutzer.query.filter_by(email=email.data).first()
        if user is not None:
            if user.id != session['benutzer_id']:
                raise ValidationError('E-Mail Adresse konnte nicht geändert werden, da bereits vergeben')

class EditPasswort(FlaskForm):
    passwort1 = PasswordField('Passwort', validators=[DataRequired(), EqualTo('passwort2', message='Eingabe stimmt nicht')])
    passwort2 = PasswordField('wiederholen', validators=[DataRequired()])
    submit_pw = SubmitField('speichern')

class BenutzerAnlegen(FlaskForm):
    benutzer = StringField('Name', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[DataRequired(), Email()])
    passwort1 = PasswordField('Passwort', validators=[DataRequired(), EqualTo('passwort2', message='Eingabe stimmt nicht')])
    passwort2 = PasswordField('wiederholen', validators=[DataRequired()])
    submit = SubmitField('speichern')

    # Prüfung auf doppelte Benutzernamen deaktiviert, da eindeutige Eigenschaft die E-Mail Adresse ist
    # def validate_benutzer(self, benutzer):
    #     benutzer = Benutzer.query.filter_by(benutzer=benutzer.data).first()
    #     if benutzer is not None:
    #         raise ValidationError('Bitte einen anderen Benutzernamen verwenden')
        
    def validate_email(self, email):
        benutzer = Benutzer.query.filter_by(email=email.data).first()
        if benutzer is not None:
            raise ValidationError('Bitte einen anderen E-Mail Adresse verwenden')