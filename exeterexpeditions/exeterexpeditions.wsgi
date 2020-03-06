#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/exeterexpeditions/")

activate_this = '/var/www/exeterexpeditions/exeterexpeditions/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from exeterexpeditions import app as application
