import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app
from app import applog
#from app import db

import pandas as pd

"""
Configuration display for a device.
"""

def tab_layout(deviceSn, device_desc):
    applog.debug('deviceSn {}, device_desc {}'.format(deviceSn, device_desc))
    if deviceSn and device_desc == 'Status: found':
        return html.Div(id='config-div', children=[ deviceSn ])
    else:
        return html.Div(id='config-div', children=[ 'No valid device' ])
