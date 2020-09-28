#! /var/www/caisovico/pages/venv/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
logging.error("-----> Python version: "+sys.version)
sys.path.insert(0, '/var/www/caisovico/venv/lib/python3.6/site-packages')
sys.path.insert(0, '/var/www/caisovico/pages')

from pages import app as application
