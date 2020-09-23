import datetime

from flask import render_template, flash, redirect, url_for

from pages import app
from pages.models import Utente
from pages.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/rifugio')
@app.route('/rifugio/rifugio.html')
def rifugio():
    return render_template('rifugio.html')

@app.route('/rifugio/percorsi')
@app.route('/rifugio/rifugio-percorsi/rifugio-percorsi.html')
def rifugio_percorsi():
    return render_template('rifugio-percorsi.html')

@app.route('/rifugio/webcams')
@app.route('/rifugio/webcam/webcam.html')
def rifugio_webcams():
    return render_template('rifugio-webcams.html')

@app.route('/rifugio/storia')
@app.route('/rifugio/rifugio-storia/rifugio-storia.html')
def rifugio_storia():
    return render_template('rifugio-storia.html')

@app.route('/rifugio/foto')
@app.route('/rifugio/rifugio-lavori/rifugio-lavori.html')
def rifugio_foto():
    return render_template('rifugio-foto.html')


@app.route('/sezione')
@app.route('/sezione/sezione.html') # Backward compatibility
def sezione():
    return render_template('sezione.html')

@app.route('/programmi')
@app.route('/programmi/programmi.html') # Backward compatibility
def programmi():
    return render_template('programmi.html')

@app.route('/bacheca')
@app.route('/bacheca/bacheca.html') # Backward compatibility
def bacheca():
    return render_template('bacheca.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Utente.query.filter_by(username=login_form.username.data).first()

        #if user is None or not user.check_password(login_form.password.data):
        #    flash('Nome utente o password errati')
        #    return redirect(url_for('login'))

        login_user(user)
        return redirect('/')

    return render_template('login.html', form=login_form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/index')






@app.errorhandler(401) 
def unauthorized(e):
  return render_template("401.html") 

@app.errorhandler(403) 
def forbidden(e):
  return render_template("403.html") 

@app.errorhandler(404) 
def not_found(e):
  return render_template("404.html") 

@app.errorhandler(405) 
def method_not_allowed(e):
  return render_template("405.html")

@app.errorhandler(500) 
def internal_error(e):
  return render_template("500.html") 
