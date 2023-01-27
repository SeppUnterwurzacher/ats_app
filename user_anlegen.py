from app import app, db
from app.models import Geraete, Kurzpruefung, Feuerwehren, Benutzer

neuer_benutzer = Benutzer()

print ("Benutzer Name eingeben:")
neuer_benutzer.name = input()

print("Email eingeben:")
neuer_benutzer.email

print('Feuerwehr id eingeben')