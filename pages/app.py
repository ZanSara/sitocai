#! /var/www/caisovico/pages/venv/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/caisovico/apps/prenotazioni/venv/lib/python3.6/site-packages')
sys.path.insert(0, '/var/www/caisovico/apps/prenotazioni')

from pages import app as application
