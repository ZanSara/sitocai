import os
from pathlib import Path
basedir = str((Path(__file__).parent).absolute())

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "sadcmwljcnqacjnalkjfhwliufhekjsnca"

    # Set DATABASE_URL to something like DATABASE_URL=mysql://nomeutente:pwdutente@localhost/nomedb
    with open(basedir+'/sqlalchemy.conf', 'r') as file:
        SQLALCHEMY_DATABASE_URI = file.read().replace('\n', '')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
