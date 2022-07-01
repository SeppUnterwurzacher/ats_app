from crypt import methods
from flask import render_template, url_for, redirect
from app import app
from app.forms import DruckForm, PrueferForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/auswahl')
def auswahl():
    title = "Home"
    return render_template('auswahl.html', title=title)

@app.route('/kpname', methods=['GET', 'POST'])
def kpname():
    title = "Einsatz 1"
    geraet = "Gerät 1"
    feuerwehr = "FF Trins"
    form = PrueferForm()
    if form.validate_on_submit():
        global data
        data = {'name': form.name.data}
        return redirect(url_for('kpgurte'))
    return render_template('/kp/kpname.html', title=title, geraet=geraet, feuerwehr=feuerwehr, form=form)


@app.route('/kpgurte')
def kpgurte():
    global data
    name = data["name"]
    return render_template('/kp/kpgurte.html', name=name, geraet="testgerät", feuerwehr="Testfeuerwehr", pruefer=name)


@app.route('/kpdruck', methods=['GET', 'POST'])
def kpdruck():
    global data
    name = data["name"]
    form = DruckForm()
    if form.validate_on_submit():
        data["druckl"] = form.druckl.data, 
        data["druckr"] = form.druckr.data
        return redirect(url_for('kpdicht'))
    return render_template('/kp/kpdruck.html', name=name, form=form, geraet="testgerät", feuerwehr="Testfeuerwehr", pruefer=name)


@app.route('/kpdicht')
def kpdicht():
    global data
    name = data["name"]
    return render_template('/kp/kpdicht.html', geraet="testgerät", feuerwehr="Testfeuerwehr", pruefer=name)

@app.route('/kpwarn')
def kpwarn():
    global data
    name = data["name"]
    return render_template('/kp/kpwarn.html', geraet="testgerät", feuerwehr="Testfeuerwehr", pruefer=name)