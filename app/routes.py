from flask import render_template, url_for, redirect, make_response, flash, session, request
from app import app, db
from app.forms import KPEinsatzUebung, WartNeuGeraet, LogbuchAuswahl, GeraeteLogin, WartLogin, WartQR, EditFeuerwehr, EditBenutzer, EditPasswort
from app.models import Feuerwehren, Geraete, Kurzpruefung, Benutzer
from datetime import date
import pdfkit
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.qrgenerator import qrgenerator

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('wart_login'))

@app.route('/geraete_login/<id>/', methods=['GET', 'POST'])
def geraete_login(id):
    form = GeraeteLogin()
    session['user_type'] = 'traeger' # wird benötigt damit login_user das Geraete Objekt zurück gibt
    
    geraet_selected = Geraete.query.filter_by(id=id).first()
    
    if geraet_selected is None:
        return 'Kein gültiges Gerät gewählt'
    
    if form.validate_on_submit():
        if geraet_selected.check_password(str(form.pin_geraet.data)):
            login_user(geraet_selected)
            return redirect(url_for('auswahl', id=id))
        else:
            flash('Pin stimmt nicht mit Gerät überein', 'error')
            return redirect(url_for('geraete_login', id=id))

    return render_template('geraete_login.html', id=id, geraet=geraet_selected.name_geraet, form=form)


@app.route('/auswahl/<id>')
def auswahl(id):
    title = "Auswahl"
    if current_user.is_authenticated:
        return render_template('auswahl.html', title=title, id=id, geraet=current_user.name_geraet)
    
    return ('Zugang nicht erlaubt')


@app.route('/kpstand/<id>/<grund>', methods=['GET', 'POST'])
def kpstand(id, grund):
    form = KPEinsatzUebung()

    if grund == 'Tourlich':
        kurz = "kurz"
    else:
        kurz = "normal"

    if grund == 'Uebung':
        grund = 'Übung'

    if form.validate_on_submit():
        id = Geraete.query.filter(Geraete.id==id).all()
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

        return redirect(url_for('eingetragen'))   
    if current_user.is_authenticated:
        return render_template('kpstandard.html', form=form, id=id, geraet=current_user.name_geraet, typ=current_user.typ_geraet, kurz=kurz)

    return ('Zugang nicht erlaubt')


@app.route('/eingetragen/')
def eingetragen():
    return render_template('transmit.html', geraet=current_user.name_geraet)

@app.route('/wart_login', methods=['GET', 'POST'])
def wart_login():
    # muss ich mir noch mal ansehen wie das umgesetz werden soll
    # if current_user.is_authenticated:
    #     return redirect(url_for('wartgeraete'))
        
    form = WartLogin()

    session['user_type'] = 'wart'

    if form.validate_on_submit():
        user = Benutzer.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(str(form.pw.data)):
            flash('Ungültiger Benutzer oder Passwort', 'error')
            return redirect(url_for('wart_login'))
        
        # id von Benutzer wird seperat in session abgespeichert, da login Funktion die Feuerwehr aufnimmt
        session['benutzer_id'] = user.id

        login_user(user)
        
        # next_page wäre dazu da wenn eine andere Seite als Login direkt angesteuert wurde
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('wartgeraete')
        return redirect(next_page)
    
    return render_template('wart/wart_login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('wart_login'))

@app.route('/wartgeraete', methods=['GET', 'POST'])
@login_required
def wartgeraete():
    geraete = Geraete.query.filter_by(id_feuerwehr=current_user.id).all()
    form = WartNeuGeraet()
    fw_name = current_user.name

    return render_template('/wart/atsgeraete.html', geraete=geraete, form=form, fw_name=fw_name)

@app.route('/geraetedetail/<id>', methods=['GET', 'POST'])
@login_required
def geraetedetail(id):
    form = WartNeuGeraet()
    geraet = Geraete.query.filter(Geraete.id==id).first()
  

    if form.validate_on_submit():
        if id == '0':
            eintrag = Geraete(
                name_geraet = form.bezeichnung.data,
                typ_geraet = form.typ.data,
                yyyy_geraet = form.anschaffung.data,
                info_geraet = form.info.data,
                id_feuerwehr = current_user.id
            )

            eintrag.set_password(str(form.pin.data))

            db.session.add(eintrag)
            db.session.commit()
        
        else:
            geraet.name_geraet = form.bezeichnung.data
            geraet.typ_geraet = form.typ.data
            geraet.yyyy_geraet = form.anschaffung.data
            geraet.info_geraet = form.info.data
            
            if not form.pin.data is None:
                geraet.set_password(str(form.pin.data))

            db.session.add(geraet)
            db.session.commit()

        return redirect(url_for('wartgeraete', geraete=geraet, form=form))

    return render_template('/wart/geraetedetail.html', id=id, form=form, geraet=geraet, fw_name=current_user.name)

@app.route('/geraeteentfernen/<id>/<check>', methods=['GET', 'POST'])
@login_required
def geraeteentfernen(id, check):
    geraet = Geraete.query.filter(Geraete.id==id).first()  
    
    if check=="1":
        db.session.delete(geraet)
        db.session.commit()
        
        return redirect(url_for('wartgeraete'))

    return render_template('/wart/geraeteentfernen.html', id=id, geraet=geraet)

@app.route('/logbuch/', methods=['GET', 'POST'])
@login_required
def logbuch():
    id  = Geraete.query.filter(Geraete.id_feuerwehr==current_user.id).first()
    if id is None:
        return redirect(url_for('wartgeraete'))
    id = id.id
    
    # Jahre für Choice Input festlegen
    geraete_ff = Geraete.query.filter(Geraete.id_feuerwehr==current_user.id).with_entities(Geraete.id).all()
    year = date.today().year
    year_min = Kurzpruefung.query.filter(Kurzpruefung.id_geraet == id).with_entities(Kurzpruefung.zeit).order_by(Kurzpruefung.zeit).first()
    year_min = year_min[0].year
    year_diff = year - year_min + 1
    
    daten = Kurzpruefung.query.filter(Kurzpruefung.id_geraet==id, Kurzpruefung.zeit>='{}-01-01'.format(year), Kurzpruefung.zeit<='{}-12-31'.format(year)).all()

    typ_geraet = Geraete.query.filter(Geraete.id==id).first()
    typ_geraet = typ_geraet.typ_geraet

    form = LogbuchAuswahl()
    geraete = Geraete.query.filter(Geraete.id_feuerwehr==current_user.id).all()
    choices_geraet = [(i.id, i.name_geraet) for i in geraete]
    form.geraet.choices = choices_geraet
    choices_jahr = [(year-i, year-i) for i in range(year_diff)]
    form.year.choices = choices_jahr

    if form.validate_on_submit():
        id = form.geraet.data
        year = form.year.data
        daten = Kurzpruefung.query.filter(Kurzpruefung.id_geraet==id, Kurzpruefung.zeit>='{}-01-01'.format(year), Kurzpruefung.zeit<='{}-12-31'.format(year)).all()

        typ_geraet = Geraete.query.filter(Geraete.id==id).first()
        typ_geraet = typ_geraet.typ_geraet

        return render_template('/wart/logbuch.html', daten=daten, form=form, year=year, fw_name=current_user.name, typ_geraet=typ_geraet)

    return render_template('/wart/logbuch.html', daten=daten, form=form, year=year, fw_name=current_user.name, typ_geraet=typ_geraet)


@app.route('/pdflogbuch/<year>')
@login_required
def pdflogbuch(year):
    #year = date.today().year
    daten = []
    geraete = Geraete.query.filter(Geraete.id_feuerwehr==current_user.id).all()

    for i in geraete:
        i_daten = Kurzpruefung.query.join(Geraete, Kurzpruefung.id_geraet==Geraete.id).add_columns(Geraete.name_geraet, Geraete.typ_geraet).filter(Kurzpruefung.id_geraet==i.id, Kurzpruefung.zeit>='{}-01-01'.format(year), Kurzpruefung.zeit<='{}-12-31'.format(year)).all()
        if len(i_daten) > 0:
            daten.append(i_daten)

    if len(daten[0]) > 0:
        rendered = render_template('pdf/pdflogbuch.html', daten=daten, year=year)
        
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


@app.route('/qrdownload', methods=['GET', 'POST'])
@login_required
def qrdownload():
    form = WartQR()

    # Auswahlmöglichkeiten für Dropdown befüllen
    geraete = Geraete.query.filter(Geraete.id_feuerwehr==current_user.id).all()
    choices_geraet = [(i.id, i.name_geraet) for i in geraete]
    form.geraet.choices = choices_geraet

    if form.validate_on_submit():
        geraet_selected = Geraete.query.filter(Geraete.id==form.geraet.data).first()
        if not geraet_selected is None and geraet_selected.check_password(str(form.pin_geraet.data)):
            
            qr_code = qrgenerator(url_for('geraete_login', id=geraet_selected.id), form.pin_geraet.data, form.geraet.data)
            qr_url = url_for('static', filename=qr_code)
            return render_template('/wart/qrdownload.html', form=form, qr_url=qr_url, fw_name=current_user.name)

        else:
            flash('Pin stimmt nicht mit Gerät überein', 'error')
            return redirect(url_for('qrdownload'))

    return render_template('/wart/qrdownload.html', form=form, fw_name=current_user.name)


@app.route('/benutzer', methods=['GET', 'POST'])
@login_required
def benutzer():
    form = EditFeuerwehr()
    form_benutzer = EditBenutzer()
    form_passwort = EditPasswort()
    benutzer = Benutzer.query.filter(Benutzer.id == session['benutzer_id']).first()

    if form.validate_on_submit():
        ff_selected = Feuerwehren.query.filter(Feuerwehren.id==current_user.id).first()

        ff_selected.name = form.name.data
        ff_selected.strasse = form.strasse.data
        ff_selected.plz = form.plz.data
        ff_selected.ort = form.ort.data

        db.session.add(ff_selected)
        db.session.commit()

        current_user.name = form.name.data
        current_user.strasse = form.strasse.data
        current_user.plz = form.plz.data
        current_user.ort = form.ort.data

        return redirect(url_for('benutzer', form=form, form_benutzer=form_benutzer, form_passwort=form_passwort, fw_name=current_user.name, benutzer=benutzer))

    if form_benutzer.validate_on_submit():
        benutzer.benutzer = form_benutzer.benutzer.data
        benutzer.email = form_benutzer.email.data

        db.session.add(benutzer)
        db.session.commit()

        return redirect(url_for('benutzer', form=form, form_benutzer=form_benutzer, form_passwort=form_passwort, fw_name=current_user.name, benutzer=benutzer)) 

    if form_passwort.validate_on_submit():
        benutzer = Benutzer.query.filter(Benutzer.id == session['benutzer_id']).first()
        benutzer.set_password(form_passwort.passwort1.data)

        db.session.add(benutzer)
        db.session.commit()

        return redirect(url_for('wartgeraete', form=form, form_benutzer=form_benutzer, form_passwort=form_passwort, fw_name=current_user.name, benutzer=benutzer)) 

    return render_template('wart/benutzer.html', form=form, form_benutzer=form_benutzer, form_passwort=form_passwort, fw_name=current_user.name, benutzer=benutzer)