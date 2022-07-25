from flask import render_template, url_for, redirect
from app import app, db
from app.forms import KPEinsatzUebung
from app.models import Kurzpruefung

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/auswahl')
def auswahl():
    title = "Home"
    return render_template('auswahl.html', title=title)

@app.route('/kpstand', methods=['GET', 'POST'])
def kpstand():
    form = KPEinsatzUebung()

    if form.validate_on_submit():
        eintrag = Kurzpruefung(
            pruefer=form.name.data, 
            grund='Einsatz', 
            druck1=form.druckl.data, 
            druck2=form.druckr.data,
            dichtheit=True,
            warnsignal=True,
            id_geraet=1)

        db.session.add(eintrag)
        db.session.commit()

        return redirect(url_for('test', name=name))   

    return render_template('kpstandard.html', form=form)


@app.route('/eingetragen')
def test():
    return '<h1>Eintrag erfolgt</h1>'