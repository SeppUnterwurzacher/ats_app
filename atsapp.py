from app import app, db
from app.models import Geraete, Kurzpruefung, Feuerwehren, Benutzer

@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'Geraete': Geraete, 'Kurzpruefung': Kurzpruefung, 'Feuerwehren': Feuerwehren, 'Benutzer': Benutzer}