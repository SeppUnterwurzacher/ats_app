from datetime import date
from app import db

class Geraete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_geraet = db.Column(db.String(30), unique=True, nullable=False)
    typ_geraet = db.Column(db.String(15))
    yyyy_geraet = db.Column(db.Integer)

    def __repr__(self):
        return '<Geraete {}>'.format(self.name_geraet)

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