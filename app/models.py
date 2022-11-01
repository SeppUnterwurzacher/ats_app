from datetime import date
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Geraete(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_geraet = db.Column(db.String(30), unique=True, nullable=False)
    typ_geraet = db.Column(db.String(15))
    yyyy_geraet = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    id_feuerwehr = db.Column(db.Integer, db.ForeignKey('feuerwehren.id'))

    def __repr__(self):
        return '<Geraete {}>'.format(self.name_geraet)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Kurzpruefung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zeit = db.Column(db.Date, index=True, default=date.today)
    pruefer = db.Column(db.String(30), nullable=False)
    geraetetraeger = db.Column(db.String(30))
    grund = db.Column(db.String(30))
    druck1 = db.Column(db.Integer)
    druck2 = db.Column(db.Integer)
    dichtheit = db.Column(db.Boolean)
    warnsignal = db.Column(db.Boolean)
    id_geraet = db.Column(db.Integer, db.ForeignKey('geraete.id'))

    def __repr__(self):
        return '<Kurzpruefung {}>'.format(self.zeit)

class Feuerwehren(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    strasse = db.Column(db.String(30), nullable=False)
    plz = db.Column(db.Integer, nullable=False)
    ort = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Feuerwehr {}>'.format(self.name)

class Benutzer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    benutzer = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(30), nullable=False)
    id_feuerwehr = db.Column(db.Integer, db.ForeignKey('feuerwehren.id'))

    def __repr__(self):
        return '<Benutzer {}>'.format(self.benutzer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_geraet(id):
    return Geraete.query.get(int(id))