# Endpoints
import datetime

from flask import render_template, flash, redirect, url_for

from app import app
from app.models import Utente, Prenotazione
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

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

    return render_template('base.html', 
                                title="Prenotazioni",
                                year=anno_corrente, 
                                oggi=oggi, 
                                giorno_dell_anno=giorno_dell_anno,
                                calendario=calendario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Nome utente o password errati')
            return redirect(url_for('login'))
        login_user(user)
        return redirect('/index')
    return render_template('login.html', form=login_form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/index')

@app.route('/prenotazioni')
@login_required
def prenotazioni():
    pass

@app.route('/ospiti')
@login_required
def ospiti():
    pass