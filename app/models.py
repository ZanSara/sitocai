import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login

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
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(500), index=True)
    telefono = db.Column(db.String(120), index=True)
    provincia = db.Column(db.String(2))
    arrivo = db.Column(db.DateTime, nullable=False, 
                default=datetime.date(datetime.date.today().year, 6, 1))
    durata = db.Column(db.Integer, nullable=False, default=1)
    posti = db.Column(db.Integer, nullable=False, default=1)
    responsabile = db.Column(db.String(120), nullable=False, default="Errore!")
    note = db.Column(db.String(1000), nullable=True)
    is_gestione = db.Column(db.Boolean, nullable=False, default=False)
    cane = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Prenotazione {}{} - {}, {} giorni, {} persone>'.format(
                                    self.nome, 
                                    " (gestore)" if self.gestione else "",
                                    self.arrivo,
                                    self.durata,
                                    self.posti
                                )    