from flask import Flask

# Inits the app and makes it available to all the components
app = Flask(__name__)

# Loads the endpoints
from app import routes