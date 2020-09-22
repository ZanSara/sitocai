import datetime

from flask import render_template, flash, redirect, url_for

from pages import app
from pages.models import Utente
from pages.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required



@app.route('/')
@app.route('/index')
@app.route('/index.html') # Backward compatibility
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()

        #if user is None or not user.check_password(login_form.password.data):
        #    flash('Nome utente o password errati')
        #    return redirect(url_for('login'))

        login_user(user)
        return redirect('/index')

    return render_template('login.html', form=login_form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route('/prenotazioni', methods=["GET", "POST"])
@login_required
def prenotazioni():
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
        return render_template('tabella-prenotazioni.html',
            title = "Lista Prenotazioni per Gestore",
            anno = anno,
            form = parametri_form,
            num_prenotazioni = 0,
            num_gestioni = 0,
            lista_prenotazioni = [],
            calendario = calendario)

    return render_template('tabella-parametri.html', 
        title = "Lista Prenotazioni per Gestore",
        anno = anno,
        form = parametri_form)


@app.route('/ospiti', methods=["GET", "POST"])
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

        return render_template('tabella-ospiti.html', 
            title = "Lista Ospiti al Rifugio Del Grande - Stagione {}".format(anno),
            anno = anno,
            form = parametri_form,
            num_prenotazioni = 0,
            num_gestioni = 0,
            prenotazioni = [])

    return render_template('tabella-parametri.html', 
        title = "Lista Ospiti al Rifugio Del Grande - Stagione {}".format(anno),
        anno = anno,
        form = parametri_form,)
