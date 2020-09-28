import datetime

from flask import render_template, flash, redirect, url_for, request

from pages import app
from pages.models import Utente
from pages.forms import LoginForm
from pages.meteo import convert_meteo_data
from flask_login import current_user, login_user, logout_user, login_required

import csv
import json
import datetime
from pathlib import Path
from urllib.request import urlopen


def double_render_template(url, **kwargs):
    if request.url.endswith('/en'):
        return render_template('en/'+url, url=request.url.replace('/en', ''), **kwargs)

    if request.url.endswith("_eng.html"):
        return render_template('en/'+url, url=request.url.replace('"_eng.html', '.html'), **kwargs)

    else:
        return render_template(url, url=request.url+"/en", **kwargs)

@app.route('/')
@app.route('/en')
@app.route('/index.html')
def index():
    return double_render_template('index.html', selected="home")

@app.route('/rifugio')
@app.route('/rifugio/rifugio.html')
@app.route('/rifugio/en')
@app.route('/rifugio/rifugio_eng.html')
def rifugio():
    return double_render_template('rifugio.html', selected="rifugio")

@app.route('/rifugio/sentieri')
@app.route('/rifugio/rifugio-percorsi/rifugio-percorsi.html')
@app.route('/rifugio/sentieri/en')
@app.route('/rifugio/rifugio-percorsi/rifugio-percorsi_eng.html')
def rifugio_sentieri():
    return double_render_template('rifugio-sentieri.html', selected="rifugio_sentieri")

@app.route('/rifugio/webcam')
@app.route('/rifugio/webcam/webcam.html')
@app.route('/rifugio/webcam/en')
def rifugio_webcams():
    # Read the JSON
    response = urlopen("http://www.caisovico.it/wm/wc2/meteo/wflexp.json")
    data_json = json.loads(response.read())

    response = urlopen("http://www.caisovico.it/wm/wc2/meteo/realtime.txt").read()
    realtime_data = response.decode('utf-8').split(" ")
    realtime_header = "date time temp_now hum_now ? ? wind_now ? rain_now ? pressure wind_dir ? wind_unit temp_unit ba_unit rain_unit ? ? rain_month rain_year ? ? ? wind_chill ? temp_max temp_max_time temp_min temp_min_time gust_speed gust_speed_time gust_speed gust_speed_time pressure_max pressure_max_time pressure_min pressure_min_time ? ? ? heat_index ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?".split(" ")
    realtime = {key: value for key, value in zip(realtime_header, realtime_data)}
    print(realtime)
    
    data = convert_meteo_data(data_json, realtime)
    
    dati_string = json.dumps(data_json, indent=4)
    data_string = json.dumps(data, indent=4)
    # Render
    return double_render_template('rifugio-webcam.html', selected="rifugio_webcam", dati_meteo=data_string, dati_string=dati_string)


@app.route('/rifugio/bivacco')
@app.route('/rifugio/rifugio-chiuso/rifugio-chiuso.html')
@app.route('/rifugio/bivacco/en')
@app.route('/rifugio/rifugio-chiuso/rifugio-chiuso_eng.html')
def rifugio_bivacco():
    return double_render_template('rifugio-bivacco.html', selected="rifugio_bivacco")

@app.route('/rifugio/storia')
@app.route('/rifugio/rifugio-storia/rifugio-storia.html')
@app.route('/rifugio/storia/en')
@app.route('/rifugio/rifugio-storia/rifugio-storia_eng.html')
def rifugio_storia():
    return double_render_template('rifugio-storia.html', selected="rifugio_storia")


@app.route('/sezione')
@app.route('/sezione/sezione.html')
@app.route('/sezione/en')
@app.route('/sezione/sezione_eng.html')
def sezione():
    return double_render_template('sezione.html', selected="sezione")

@app.route('/sezione/quote')
@app.route('/sezione/quote/en')
@app.route('/sezione/sezione-quote.html')
@app.route('/sezione/sezione-quote_eng.html')
def sezione_quote():
    return double_render_template('sezione-quote.html', selected="sezione_quote")

@app.route('/sezione/storia')
@app.route('/sezione/sezione-storia.html')
@app.route('/sezione/storia/en')
@app.route('/sezione/sezione-storia_eng.html')
def sezione_storia():
    return double_render_template('sezione-storia.html', selected="sezione_storia")

@app.route('/sezione/bacheca')
@app.route('/bacheca/bacheca.html')
def sezione_bacheca():
    return render_template('sezione-bacheca.html', selected="sezione_bacheca")

@app.route('/sezione/programmi')
@app.route('/programmi/programmi.html')
def sezione_programmi():
    return render_template('sezione-programmi.html', selected="sezione_programmi")



@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()

        #if user is None or not user.check_password(login_form.password.data):
        #    flash('Nome utente o password errati')
        #    return redirect(url_for('login'))

        login_user(user)
        return redirect('/')

    return render_template('login.html', form=login_form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/index')






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
