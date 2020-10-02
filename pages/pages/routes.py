import datetime

from flask import render_template, redirect, url_for, request

from pages import app
from pages.models import Utente, Prenotazione
from pages.forms import LoginForm, ParametriForm
from pages.meteo import convert_meteo_data
from pages.prenotazioni import login, calendario, giorno_dell_anno, turno, ospiti, crea_prenotazione, disponibilita
from flask_login import current_user, logout_user, login_required

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
    prenotazione = None
    if request.method == "POST":
        prenotazione = crea_prenotazione(request)
    return render_template('prenotazioni/prenotazioni.html', 
                                title="Prenotazioni", 
                                selected="rifugio_prenotazioni",
                                form=LoginForm(),
                                oggi=datetime.date.today(), 
                                giorno_dell_anno=giorno_dell_anno(),
                                calendario=calendario(),
                                nuova_prenotazione=prenotazione)


@app.route('/rifugio/prenotazioni/login', methods=['POST'])
def prenotazioni_login():
    login()
    return redirect(url_for('prenotazioni'))

@app.route('/rifugio/prenotazioni/logout', methods=['GET'])
@login_required
def prenotazioni_logout():
    logout_user()
    return redirect(url_for('prenotazioni'))

@app.route('/rifugio/prenotazioni/disponibilita', methods=['GET'])
@login_required
def prenotazioni_disponibilita():
    arrivo = int(request.args['arrivo'])*0.001
    arrivo = datetime.datetime.fromtimestamp(arrivo).date()
    durata = int(request.args['durata'])
    return disponibilita(arrivo, durata)

@app.route('/rifugio/prenotazioni/turno', methods=["GET", "POST"])
@login_required
def prenotazioni_turno():
    if request.method == "POST":
        return render_template('prenotazioni/turno.html', 
                                title="Turno", 
                                selected="rifugio_prenotazioni",
                                **turno(request))
    return redirect('/rifugio/prenotazioni')

@app.route('/rifugio/prenotazioni/ospiti')
@login_required
def prenotazioni_ospiti():
    return render_template('prenotazioni/ospiti.html', 
            title = "Ospiti",
            selected="rifugio_prenotazioni",
            anno = datetime.date.today().year,
            **ospiti(request))





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
    '/caiprenota': '/rifugio/prenotazioni',
    '/caiprenota/': '/rifugio/prenotazioni',
    '/caiprenota/login': '/rifugio/prenotazioni',
    '/caiprenota/login/': '/rifugio/prenotazioni',
    '/caiprenota/calendar': '/rifugio/prenotazioni',
    '/caiprenota/calendar/': '/rifugio/prenotazioni',
    '/caiprenota/prenotazioni': '/rifugio/prenotazioni',
    '/caiprenota/prenotazioni/': '/rifugio/prenotazioni',
    '/caiprenota/ospiti': '/rifugio/prenotazioni/ospiti',
    '/caiprenota/ospiti/': '/rifugio/prenotazioni/ospiti',
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
