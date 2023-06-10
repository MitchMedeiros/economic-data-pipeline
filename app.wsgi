#!/var/www/backtest.fi/econ_venv/bin/python3.10

import logging
import sys

logging.basicConfig(stream=sys.stderr)

# Provide the root directory of the app
sys.path.insert(0, "/var/www/backtest.fi/economic_data/")

# Specify the webserver object as application for mod_wsgi. Needs to be below sys.path.insert
from main import server as application
