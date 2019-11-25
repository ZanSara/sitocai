# Endpoints
from flask import render_template

from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title="Prenotazioni", year="2019", authenticated=False)


@app.route('/login')
def login():
    return render_template('base.html', title="Prenotazioni", year="2019", authenticated=True)


@app.route('/logout')
def logout():
    return render_template('base.html', title="Prenotazioni", year="2019", authenticated=False)
