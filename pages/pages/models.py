import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from pages import db
from pages import login

class Utente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Utente {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   

    @login.user_loader
    def load_user(id):
        return Utente.query.get(int(id))


class Prenotazione(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(500), index=True, nullable=False)
    telefono = db.Column(db.String(120), index=True, nullable=False)
    provincia = db.Column(db.String(30), nullable=True)
    arrivo = db.Column(db.DateTime, nullable=False)
    durata = db.Column(db.Integer, nullable=False)
    partenza = db.Column(db.DateTime, nullable=False)
    posti = db.Column(db.Integer, nullable=True)
    responsabile = db.Column(db.String(120), nullable=False)
    note = db.Column(db.String(1000), nullable=True)
    gestione = db.Column(db.Boolean, nullable=False)
    cane = db.Column(db.Boolean, nullable=False)
    colore = db.Column(db.String(7), nullable=False)

    def __repr__(self):
        return '<Prenotazione {}{} - {}, {} giorni{}>'.format(
                                    self.nome, 
                                    " (gestore)" if self.gestione else "",
                                    self.arrivo,
                                    self.durata,
                                    f", {self.posti} persone" if not self.gestione else ""
                                )    
