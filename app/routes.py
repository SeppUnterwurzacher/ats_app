from flask import render_template, url_for, redirect
from app import app, db
from app.forms import KPEinsatzUebung
from app.models import Geraete, Kurzpruefung

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/auswahl/<geraet>')
def auswahl(geraet):
    title = "Home"
    return render_template('auswahl.html', title=title, geraet=geraet)

@app.route('/kpstand/<geraet>', methods=['GET', 'POST'])
def kpstand(geraet):
    form = KPEinsatzUebung()

    if form.validate_on_submit():
        id = Geraete.query.filter(Geraete.name_geraet==geraet).all()
        id = id[0].id
        eintrag = Kurzpruefung(
            pruefer=form.name.data, 
            grund='Einsatz', 
            druck1=form.druckl.data, 
            druck2=form.druckr.data,
            dichtheit=True,
            warnsignal=True,
            id_geraet=id)

        db.session.add(eintrag)
        db.session.commit()

        return redirect(url_for('eingetragen'))   

    return render_template('kpstandard.html', form=form, geraet=geraet)


@app.route('/eingetragen')
def eingetragen():
    return '<h1>Eintrag erfolgt</h1>'