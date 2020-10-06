import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Accedi')

class ParametriForm(FlaskForm):
    inizio = DateField('Inizio', format='%Y-%m-%d', validators=[DataRequired()])
    fine = DateField('Fine', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Invia')

class PrenotazioneForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    telefono = StringField('Telefono', validators=[DataRequired()])
    provincia = StringField('Provincia', validators=[DataRequired()])
    arrivo = DateField('Inizio', format='%Y-%m-%d', validators=[DataRequired()])
    durata = IntegerField('Durata', validators=[DataRequired()])
    partenza = DateField('Partenza', validators=[DataRequired()])
    posti = IntegerField('Posti')  # Non necessario se e' una gestione
    responsabile = StringField('Responsabile', validators=[DataRequired()])
    note = StringField('Note')
    gestione = BooleanField('Gestione')
    cane = BooleanField('Cane')
    colore = StringField('Colore')