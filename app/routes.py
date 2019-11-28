# Endpoints
import datetime

from flask import render_template

from app import app
from app.models import Prenotazione

import locale
locale.setlocale(locale.LC_ALL, 'it_IT')


@app.route('/')
@app.route('/index')
def index():
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

    return render_template('base.html', title="Prenotazioni", authenticated=False,
                                year=anno_corrente, oggi=oggi, giorno_dell_anno=giorno_dell_anno,
                                calendario=calendario)


@app.route('/login')
def login():
    return render_template('base.html', title="Prenotazioni", year="2019", authenticated=True)


@app.route('/logout')
def logout():
    return render_template('base.html', title="Prenotazioni", year="2019", authenticated=False)


@app.route('/prenotazioni')
def prenotazioni():
    pass

@app.route('/ospiti')
def ospiti():
    pass