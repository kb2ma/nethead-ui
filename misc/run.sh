#!/bin/sh
# Run NetHead UI

export FLASK_APP=src/nethead.py
export FLASK_ENV=development
# Contains configuration settings to override the defaults in app_conf.py.
#export DI_CONF_FILE=../nethead.conf

flask run --host=0.0.0.0 --port=8050 --with-threads
