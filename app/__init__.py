from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# Load configuration
app.config.from_object(Config)
# Database management
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Authentication management
login = LoginManager(app)

# Setup locale
import locale
locale.setlocale(locale.LC_ALL, 'it_IT')

from app import routes, models