"""
Copyright 2020 Ken Bannister

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import dash
import dash_bootstrap_components as dbc
import flask
import logging
from logging.handlers import TimedRotatingFileHandler
import sqlalchemy as sqla

"""Application level setup for for NetHead UI Dash/Flask application."""

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY])

# initialize configuration constants
try:
    server.config.from_envvar('NETHEAD_CONF_FILE')
except:
    logstr = 'NetHead UI conf file missing or unreadable; using defaults'
    logging.getLogger().warning(logstr)

# set up logging
_handler = TimedRotatingFileHandler(server.config['LOGGING_PATHNAME'], 
                                    when='D')
_fmt_str = '[%(asctime)s,%(msecs)03d] %(name)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
_fmt = logging.Formatter(fmt=_fmt_str, datefmt='%H:%M:%S')
_handler.setFormatter(_fmt)

logging.getLogger().addHandler(_handler)
logging.getLogger().setLevel(logging.DEBUG)
logging.captureWarnings(True)

# Set the stdout/stderr handler(s) for Werkzeug and app (Flask) to
# WARNING so that output only contain important log messages.
for h in logging.getLogger('werkzeug').handlers:
    h.setLevel(logging.WARNING)
for h in logging.getLogger('app').handlers:
    h.setLevel(logging.WARNING)

# applog provides a convenient name when logging
applog = server.logger
applog.info('Logging set up OK')

app.title = 'Nethead'
# for multi-page (or tabbed) apps
app.config.suppress_callback_exceptions = True

# Config database access
connStr = 'sqlite:///{}'
db = sqla.create_engine(connStr.format('/home/kbee/dev/leshan/share/nethead.db'))
applog.info('Initialized config db: {}'.format(db))
