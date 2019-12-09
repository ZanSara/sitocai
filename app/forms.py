import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Accedi')

class ParametriForm(FlaskForm):
    inizio = DateField('Inizio', format='%d-%m-%Y', validators=[DataRequired()])
    fine = DateField('Fine', format='%d-%m-%Y', validators=[DataRequired()])
    submit = SubmitField('Invia')