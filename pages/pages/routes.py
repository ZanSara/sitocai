import datetime

from flask import render_template, flash, redirect, url_for, request

from pages import app
from pages.models import Utente, Prenotazione
from pages.forms import LoginForm, ParametriForm
from pages.functions import convert_meteo_data
from flask_login import current_user, login_user, logout_user, login_required

import csv
import json
import datetime
from pathlib import Path
from urllib.request import urlopen


def double_render_template(url, **kwargs):
    if request.url.endswith('/en'):
        return render_template('en/'+url, url=request.url.replace('/en', ''), **kwargs)
    else:
        return render_template(url, url=request.url+"/en", **kwargs)

@app.route('/')
@app.route('/en')
def index():
    return double_render_template('index.html', title="Home", selected="home")

@app.route('/rifugio')
@app.route('/rifugio/en')
def rifugio():
    return double_render_template('rifugio.html', title="Rifugio", selected="rifugio")

@app.route('/rifugio/sentieri')
@app.route('/rifugio/sentieri/en')
def rifugio_sentieri():
    return double_render_template('rifugio-sentieri.html', title="Sentieri", selected="rifugio_sentieri")

@app.route('/rifugio/webcam')
@app.route('/rifugio/webcam/en')
def rifugio_webcams():
    # Read the JSON
    response = urlopen("http://www.caisovico.it/wm/wc2/meteo/wflexp.json")
    data_json = json.loads(response.read())

    response = urlopen("http://www.caisovico.it/wm/wc2/meteo/realtime.txt").read()
    realtime_data = response.decode('utf-8').split(" ")
    realtime_header = "date time temp_now hum_now ? ? wind_now ? rain_now ? pressure wind_dir ? wind_unit temp_unit ba_unit rain_unit ? ? rain_month rain_year ? ? ? wind_chill ? temp_max temp_max_time temp_min temp_min_time gust_speed gust_speed_time gust_speed gust_speed_time pressure_max pressure_max_time pressure_min pressure_min_time ? ? ? heat_index ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?".split(" ")
    realtime = {key: value for key, value in zip(realtime_header, realtime_data) if key != "?"}
    
    data = convert_meteo_data(data_json, realtime)
    
    dati_string = json.dumps(data_json, indent=4)
    data_string = json.dumps(data, indent=4)
    # Render
    return double_render_template('rifugio-webcam.html', title="Webcam", selected="rifugio_webcam", 
            dati_meteo=data_string, dati_string=dati_string)


@app.route('/rifugio/bivacco')
@app.route('/rifugio/bivacco/en')
def rifugio_bivacco():
    return double_render_template('rifugio-bivacco.html', title="Bivacco", selected="rifugio_bivacco")

@app.route('/rifugio/storia')
@app.route('/rifugio/storia/en')
def rifugio_storia():
    return double_render_template('rifugio-storia.html', title="Storia del Rifugio", selected="rifugio_storia")


@app.route('/sezione')
@app.route('/sezione/en')
def sezione():
    return double_render_template('sezione.html', title="Sezione", selected="sezione")

@app.route('/sezione/quote')
@app.route('/sezione/quote/en')
def sezione_quote():
    return double_render_template('sezione-quote.html', title="Quote", selected="sezione_quote")

@app.route('/sezione/storia')
@app.route('/sezione/storia/en')
def sezione_storia():
    return double_render_template('sezione-storia.html', title="Storia della Sezione", selected="sezione_storia")

@app.route('/sezione/bacheca')
def sezione_bacheca():
    return render_template('sezione-bacheca.html', title="Bacheca", selected="sezione_bacheca")

@app.route('/sezione/programmi')
@app.route('/programmi/programmi.html')
def sezione_programmi():
    return render_template('sezione-programmi.html', title="Programmi", selected="sezione_programmi")




@app.route('/rifugio/prenotazioni', methods=['GET', 'POST'])
def prenotazioni():
    # Calendario
    oggi = datetime.date(2019, 6, 3) #datetime.date.today()\
    anno_corrente = oggi.year
    giorno_dell_anno = (oggi - datetime.date(anno_corrente, 1, 1)).days

    inizio_gestione = datetime.date(anno_corrente, 6, 1)
    fine_gestione = datetime.date(anno_corrente, 10, 1)
    giorni_gestione = [inizio_gestione + datetime.timedelta(days=x) 
                        for x in range((fine_gestione-inizio_gestione).days)]
    calendario = {
        giorno : {
            "gestore" : None,  #get_gestore(giorno),
            "prenotazioni" : [], #get_prenotazioni(giorno),
        }
    for giorno in giorni_gestione}

    # Login
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Nome utente o password errati')
        else:
            login_user(user)

    return render_template('prenotazioni/prenotazioni.html', 
                                title="Prenotazioni", 
                                selected="rifugio_prenotazioni",
                                form=login_form,
                                year=anno_corrente, 
                                oggi=oggi, 
                                giorno_dell_anno=giorno_dell_anno,
                                calendario=calendario)

@app.route('/rifugio/prenotazioni/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()

        if user is None or not user.check_password(login_form.password.data):
            flash('Nome utente o password errati')
            return redirect(url_for('login'))

        login_user(user)
        return redirect('/rifugio/prenotazioni')

    return render_template('prenotazioni/login.html', form=login_form)

@app.route('/rifugio/prenotazioni/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/rifugio/prenotazioni')

@app.route('/rifugio/prenotazioni/calendario', methods=["GET", "POST"])
@login_required
def calendario():
    anno = datetime.date.today().year
    parametri_form = ParametriForm()
    if parametri_form.validate_on_submit():

        # Validazione date
        if parametri_form.inizio.data and parametri_form.inizio.data < datetime.date(anno, 6, 1):
            flash("La data di inizio non puo' precedere la data di inizio stagione (01-06-{}).".format(anno))
            return redirect('/prenotazioni')

        if parametri_form.fine.data and parametri_form.fine.data > datetime.date(anno, 9, 30):
            flash("La data di fine non puo' seguire la data di fine stagione (30-09-{}).".format(anno))
            return redirect('/prenotazioni')

        if parametri_form.inizio.data and parametri_form.fine.data \
            and parametri_form.inizio.data > parametri_form.fine.data:
            flash("La data di fine non puo' precedere la data di inizio.".format(anno))
            return redirect('/prenotazioni')

        giorno_dell_anno = (datetime.date.today() - datetime.date(anno, 1, 1)).days
        inizio_gestione = datetime.date(anno, 6, 1)
        fine_gestione = datetime.date(anno, 10, 1)
        giorni_gestione = [inizio_gestione + datetime.timedelta(days=x) 
                            for x in range((fine_gestione-inizio_gestione).days)]
        calendario = { giorno : [] for giorno in giorni_gestione}
        return render_template('prenotazioni/tabella-prenotazioni.html',
            title = "Lista Prenotazioni per Gestore",
            anno = anno,
            form = parametri_form,
            num_prenotazioni = 0,
            num_gestioni = 0,
            lista_prenotazioni = [],
            calendario = calendario)

    return render_template('prenotazioni/tabella-parametri.html', 
        title = "Lista Prenotazioni per Gestore",
        anno = anno,
        form = parametri_form)

@app.route('/rifugio/prenotazioni/ospiti', methods=["GET", "POST"])
@login_required
def ospiti():
    anno = datetime.date.today().year
    parametri_form = ParametriForm()
    if parametri_form.validate_on_submit():

        # Validazione date
        if parametri_form.inizio.data and parametri_form.inizio.data < datetime.date(anno, 6, 1):
            flash("La data di inizio non puo' precedere la data di inizio stagione (01-06-{}).".format(anno))
            return redirect('/ospiti')

        if parametri_form.fine.data and parametri_form.fine.data > datetime.date(anno, 9, 30):
            flash("La data di fine non puo' seguire la data di fine stagione (30-09-{}).".format(anno))
            return redirect('/ospiti')

        if parametri_form.inizio.data and parametri_form.fine.data \
            and parametri_form.inizio.data > parametri_form.fine.data:
            flash("La data di fine non puo' precedere la data di inizio.".format(anno))
            return redirect('/ospiti')

        return render_template('prenotazioni/tabella-ospiti.html', 
            title = "Lista Ospiti al Rifugio Del Grande - Stagione {}".format(anno),
            anno = anno,
            form = parametri_form,
            num_prenotazioni = 0,
            num_gestioni = 0,
            prenotazioni = [])

    return render_template('prenotazioni/tabella-parametri.html', 
        title = "Lista Ospiti al Rifugio Del Grande - Stagione {}".format(anno),
        anno = anno,
        form = parametri_form,)






# Corrispondenze tra tutte le vecchie URL e le nuove
server_name = "http://localhost:5000"
redirections = {
    '/index.html': "/",
    '/rifugio/rifugio.html': '/rifugio',
    '/rifugio/rifugio_eng.html': '/rifugio/en',
    '/rifugio/rifugio-percorsi/rifugio-percorsi.html': '/rifugio/sentieri',
    '/rifugio/rifugio-percorsi/rifugio-percorsi_eng.html': '/rifugio/sentieri/en', 
    '/rifugio/webcam/webcam.html': '/rifugio/webcam',
    '/rifugio/rifugio-chiuso/rifugio-chiuso.html': '/rifugio/bivacco',
    '/rifugio/rifugio-chiuso/rifugio-chiuso_eng.html': '/rifugio/bivacco/en',
    '/rifugio/rifugio-storia/rifugio-storia.html': '/rifugio/storia',
    '/rifugio/rifugio-storia/rifugio-storia_eng.html': '/rifugio/storia/en',
    '/sezione/sezione.html': '/sezione',
    '/sezione/sezione_eng.html':'/sezione/en',
    '/sezione/sezione-quote.html':'/sezione/quote',
    '/sezione/sezione-quote_eng.html':'/sezione/quote/en',
    '/sezione/sezione-storia.html':'/sezione/storia',
    '/sezione/sezione-storia_eng.html':'/sezione/storia/en',
    '/bacheca/bacheca.html': '/sezione/bacheca',
    '/programmi/programmi.html': '/sezione/programmi',
}

@app.errorhandler(401) 
def unauthorized(e):
    if '/en/' in request.url:
        return render_template("en/401.html") 
    else:
        return render_template("401.html") 

@app.errorhandler(403) 
def forbidden(e):
    if '/en/' in request.url:
        return render_template("en/403.html") 
    else:
        return render_template("403.html") 

@app.errorhandler(404) 
def not_found(e):
    try:
        return redirect(redirections[request.url.replace(server_name, "")])
    except KeyError:
        # The URL is not in the redirections list
        if '/en/' in request.url:
            return render_template("en/404.html") 
        else:
            return render_template("404.html") 

@app.errorhandler(405) 
def method_not_allowed(e):
    if '/en/' in request.url:
        return render_template("en/405.html") 
    else:
        return render_template("405.html") 

@app.errorhandler(500) 
def internal_error(e):
    if '/en/' in request.url:
        return render_template("en/500.html") 
    else:
        return render_template("500.html") 
