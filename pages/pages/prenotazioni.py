import random
import datetime

from flask import flash
from flask_login import login_user

from pages import db
from pages.models import Utente, Prenotazione
from pages.forms import LoginForm, ParametriForm, PrenotazioneForm


INIZIO_STAGIONE = datetime.date(datetime.date.today().year, 6, 1)
FINE_STAGIONE = datetime.date(datetime.date.today().year, 10, 1)


def valida_date(arrivo, durata):
    errors = []
    if not arrivo:
        errors.append("E' necessario specificare la data di arrivo.")
    if not durata:
        errors.append("E' necessario specificare la durata del soggiorno.")

    if arrivo and durata:
        if arrivo < INIZIO_STAGIONE:
            errors.append(f"La data di arrivo ({arrivo.strftime('%d/%m/%Y')}) "+
                        f"non puo' precedere la data di inizio stagione ({INIZIO_STAGIONE.strftime('%d/%m/%Y')}).")
        partenza = arrivo + datetime.timedelta(days=durata)
        if partenza > FINE_STAGIONE:
            errors.append(f"La data di partenza ({partenza.strftime('%d/%m/%Y')}) " +
                        f"non puo' seguire la data di fine stagione ({FINE_STAGIONE.strftime('%d/%m/%Y')}).")
    return errors


def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Nome utente o password errati')
        else:
            login_user(user)


def giorno_dell_anno():
    return (datetime.date.today() - datetime.date(datetime.date.today().year, 1, 1)).days


def calendario():
    #Prenotazione.query.delete()
    for p in Prenotazione.query.all():
        print(p)

    oggi = datetime.date.today()
    giorno_dell_anno = (oggi - datetime.date(oggi.year, 1, 1)).days
    giorni_gestione = [INIZIO_STAGIONE + datetime.timedelta(days=x) 
                        for x in range((FINE_STAGIONE-INIZIO_STAGIONE).days)]
    return {
        giorno : {
            "gestore" : Prenotazione.query.filter_by(gestione=True).filter(Prenotazione.arrivo < giorno).filter(Prenotazione.partenza > giorno).first(),
            "prenotazioni" : Prenotazione.query.filter_by(gestione=False).filter(Prenotazione.arrivo <= giorno).filter(Prenotazione.partenza > giorno).all(),
        }
    for giorno in giorni_gestione}


def crea_prenotazione(request):
    form = PrenotazioneForm(request.form)
    form.partenza.data = form.arrivo.data + datetime.timedelta(days=form.durata.data)  # NECESSARY
    form.colore.data = random.choice(['#FFFFFF', "#FF0000", "#00FF00", "#00FFFF", "#FFFF00", '#CCCCCC'])
    response = {'errors': []}

    # Validazione
    if not form.validate_on_submit():
        response['errors'].append("I dati di prenotazione non sono validi.")
    for error in valida_date(form.arrivo.data, form.durata.data):
        response['errors'].append(error)
    if not form.gestione and not form.posti:
        response['errors'].append(f"E' necessario specificare il numero di posti letto prenotati.")
    if len(response['errors']) > 0:
        return response

    data = {key: value for key, value in form.data.items() if key != "csrf_token"}
    prenotazione = Prenotazione(**data)
    db.session.add(prenotazione)
    db.session.commit()

    return {'errors': [], 'id': prenotazione.id}


def disponibilita(arrivo, durata):
    response = {'errors': valida_date(arrivo, durata)}
    if len(response['errors']) == 0:
        response['letti'] = 3
        response['emergenza'] = 6
    return response


def turno(request):
    parametri_form = ParametriForm(request.form)
    if not parametri_form.validate_on_submit():
        return {'errors': ["Il form non e' valido."]}

    anno = datetime.date.today().year
    inizio_turno = parametri_form.inizio.data
    fine_turno = parametri_form.fine.data
    response = {
        'errors': [],
        'inizio_turno': inizio_turno.strftime('%d/%m/%Y'),
        'fine_turno': fine_turno.strftime('%d/%m/%Y'),
    }
    if inizio_turno < INIZIO_STAGIONE:
        response['errors'].append("La data di inizio turno ({}) non puo' precedere la data di inizio stagione ({}).".format(
                                    response['inizio_turno'], INIZIO_STAGIONE.strftime("%d/%m/%Y"),))

    if parametri_form.fine.data and parametri_form.fine.data > FINE_STAGIONE:
        response['errors'].append("La data di fine turno ({}) non puo' seguire la data di fine stagione ({}).".format(
                                    response['fine_turno'], FINE_STAGIONE.strftime("%d/%m/%Y")))
        
    if parametri_form.inizio.data and parametri_form.fine.data \
        and parametri_form.inizio.data > parametri_form.fine.data:
        response['errors'].append("La data di fine ({}) non puo' precedere la data di inizio ({}).".format(
                                    response['inizio_turno'], response['fine_turno']))

    if len(response['errors']) == 0:
        giorni_turno = [inizio_turno + datetime.timedelta(days=x) 
                            for x in range((fine_turno-inizio_turno).days)]

        response['num_prenotazioni'] = 0
        response['lista_prenotazioni'] = []
        response['calendario'] = { giorno : [] for giorno in giorni_turno}
        
    return response


def ospiti(request):
    anno = datetime.date.today().year
    response = {}
    response['num_prenotazioni'] = 0
    response['num_gestioni'] = 0
    response['lista_prenotazioni'] = []
    return response


        
