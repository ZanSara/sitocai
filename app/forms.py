from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Accedi')

class ParametriForm(FlaskForm):
    inizio = DateField('Inizio', validators=[DataRequired()])
    fine = DateField('Fine', validators=[DataRequired()])
    submit = SubmitField('Invia')
    
    def validate_on_submit(self):
        result = super(ParametriForm, self).validate()
        if self.inizio.data and self.fine.data and (self.inizio.data > self.fine.data):
            return False
        else:
            return result