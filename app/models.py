from app import db

class Prenotazione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(500), index=True)
    telefono = db.Column(db.String(120), index=True)
    provincia = db.Column(db.String(2))
    arrivo = db.Column(db.DateTime, nullable=False)
    durata = db.Column(db.Integer, nullable=False, default=1)
    posti = db.Column(db.Integer, nullable=False, default=1)
    responsabile = db.Column(db.String(120), nullable=False)
    note = db.Column(db.String(1000), nullable=True)
    gestori = db.Column(db.Boolean, nullable=False)
    cane = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Prenotazione {}{}>'.format(self.nome, " (gestore)" if self.gestione else "")    