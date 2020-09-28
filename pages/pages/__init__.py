from flask import Flask
from pages.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Authentication management
login = LoginManager(app)
# Load configuration
app.config.from_object(Config)
# Database management
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setup locale
import locale
locale.setlocale(locale.LC_ALL, 'it_IT')

from pages import routes, models
