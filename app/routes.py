from curses import flash
from flask import render_template, url_for, redirect, make_response, flash
from app import app, db
from app.forms import KPEinsatzUebung, WartNeuGeraet, LogbuchAuswahl, GeraeteLogin
from app.models import Geraete, Kurzpruefung
from datetime import date
import pdfkit
from flask_login import current_user, login_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/geraete_login/<geraet>/', methods=['GET', 'POST'])
def geraete_login(geraet):
    form = GeraeteLogin()
    if form.validate_on_submit():
        geraet_selected = Geraete.query.filter_by(name_geraet=geraet).first()
        if geraet_selected is None:
            return 'Kein gültiges Gerät gewählt'

        if geraet_selected.check_password(str(form.pin_geraet.data)):
            login_user(geraet_selected)
            return redirect(url_for('auswahl', geraet=geraet))
        else:
            flash('Pin stimmt nicht mit Gerät überein', 'error')
            return redirect(url_for('geraete_login', geraet=geraet))

    return render_template('geraete_login.html', geraet=geraet, form=form)


@app.route('/auswahl/<geraet>')
def auswahl(geraet):
    title = "Auswahl"
    if current_user.is_authenticated:
        return render_template('auswahl.html', title=title, geraet=geraet)
    
    return ('Zugang nicht erlaubt')


@app.route('/kpstand/<geraet>/<grund>', methods=['GET', 'POST'])
def kpstand(geraet, grund):
    form = KPEinsatzUebung()

    if grund == 'Tourlich':
        kurz = "kurz"
    else:
        kurz = "normal"

    if grund == 'Uebung':
        grund = 'Übung'

    if form.validate_on_submit():
        id = Geraete.query.filter(Geraete.name_geraet==geraet).all()
        id = id[0].id
        
        if grund == 'Tourlich':
            traeger = ""
        elif form.traeger.data == "":
            traeger = form.name.data
        else:
            traeger = form.traeger.data

        eintrag = Kurzpruefung(
            pruefer=form.name.data,
            geraetetraeger=traeger, 
            grund=grund, 
            druck1=form.druckl.data, 
            druck2=form.druckr.data,
            dichtheit=True,
            warnsignal=True,
            id_geraet=id)

        db.session.add(eintrag)
        db.session.commit()

        return redirect(url_for('eingetragen', geraet=geraet))   
    if current_user.is_authenticated:
        return render_template('kpstandard.html', form=form, geraet=geraet, kurz=kurz)

    return ('Zugang nicht erlaubt')


@app.route('/eingetragen/<geraet>')
def eingetragen(geraet):
    return render_template('transmit.html', geraet=geraet)


@app.route('/wartgeraete', methods=['GET', 'POST'])
def wartgeraete():
    geraete = Geraete.query.all()
    form = WartNeuGeraet()

    if form.validate_on_submit():
        eintrag = Geraete(
            name_geraet = form.bezeichnung.data,
            typ_geraet = form.typ.data,
            yyyy_geraet = form.anschaffung.data
        )

        db.session.add(eintrag)
        db.session.commit()

        return redirect(url_for('wartgeraete', geraete=geraete, form=form)) 

    return render_template('/wart/atsgeraete.html', geraete=geraete, form=form)

@app.route('/geraetedetail/<id>', methods=['GET', 'POST'])
def geraetedetail(id):
    form = WartNeuGeraet()
    geraet = Geraete.query.filter(Geraete.id==id).first()
  

    if form.validate_on_submit():
        if id == '0':
            eintrag = Geraete(
                name_geraet = form.bezeichnung.data,
                typ_geraet = form.typ.data,
                yyyy_geraet = form.anschaffung.data
            )

            db.session.add(eintrag)
            db.session.commit()
        
        else:
            geraet.name_geraet = form.bezeichnung.data
            geraet.typ_geraet = form.typ.data
            geraet.yyyy_geraet = form.anschaffung.data

            db.session.add(geraet)
            db.session.commit()

        return redirect(url_for('wartgeraete', geraete=geraet, form=form))

    return render_template('/wart/geraetedetail.html', id=id, form=form, geraet=geraet)

@app.route('/geraeteentfernen/<id>/<check>', methods=['GET', 'POST'])
def geraeteentfernen(id, check):
    geraet = Geraete.query.filter(Geraete.id==id).first()  
    
    if check=="1":
        db.session.delete(geraet)
        db.session.commit()
        
        return redirect(url_for('wartgeraete'))

    return render_template('/wart/geraeteentfernen.html', id=id, geraet=geraet)

@app.route('/logbuch/', methods=['GET', 'POST'])
def logbuch():
    id  = 1
    year = date.today().year
    daten = Kurzpruefung.query.filter(Kurzpruefung.id_geraet==id, Kurzpruefung.zeit>='{}-01-01'.format(year), Kurzpruefung.zeit<='{}-12-31'.format(year)).all()

    form = LogbuchAuswahl()
    geraete = Geraete.query.all()
    choices_geraet = [(i.id, i.name_geraet) for i in geraete]
    form.geraet.choices = choices_geraet
    choices_jahr = [(year-i, year-i) for i in range(20)]
    form.year.choices = choices_jahr

    if form.validate_on_submit():
        id = form.geraet.data
        year = form.year.data
        daten = Kurzpruefung.query.filter(Kurzpruefung.id_geraet==id, Kurzpruefung.zeit>='{}-01-01'.format(year), Kurzpruefung.zeit<='{}-12-31'.format(year)).all()
        return render_template('/wart/logbuch.html', daten=daten, form=form, year=year)

    return render_template('/wart/logbuch.html', daten=daten, form=form, year=year)


@app.route('/pdflogbuch/<year>')
def pdflogbuch(year):
    #year = date.today().year
    daten = []
    geraete = Geraete.query.all()

    for i in geraete:
        i_daten = Kurzpruefung.query.join(Geraete, Kurzpruefung.id_geraet==Geraete.id).add_columns(Geraete.name_geraet).filter(Kurzpruefung.id_geraet==i.id, Kurzpruefung.zeit>='{}-01-01'.format(year), Kurzpruefung.zeit<='{}-12-31'.format(year)).all()
        if len(i_daten) > 0:
            daten.append(i_daten)

    if len(daten[0]) > 0:
        rendered = render_template('pdf/pdflogbuch.html', daten=daten)
        
        options = {
            'orientation': 'Landscape'
        }

        pdf = pdfkit.from_string(rendered, False, options=options)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Dispostiion'] = 'inline; filename=output.pdf'

        return response
    else:
        return "Keine Daten vorhanden"