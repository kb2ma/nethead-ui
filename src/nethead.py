import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app
from app import applog
from app import db
from app import server

import pandas as pd

import graph
import config

"""Main/Top view for NetHead UI."""

"""Establish constant since text used for comparisons"""
DEVICE_NOT_FOUND = 'Status: not found'

def gen_device_df(device_sn):
    """Generates dataframe for a device from config db."""
    rawSql = "SELECT dv.serial_number \
        FROM device dv \
        WHERE dv.serial_number = '{}'"
    sql = rawSql.format(device_sn)

    df = pd.read_sql(sql, db)
    return df


def gen_device_status(text):
    """Generates status message"""
    return 'Status: {}'.format(text)


def serve_layout():
    tabs_styles = {
        'height': '44px'
    }
    tab_style = {
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6px',
        'fontWeight': 'bold'
    }

    tab_selected_style = {
        'borderTop': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#336699',
        'color': 'white',
        'fontWeight': 'bold',
        'padding': '6px'
    }

    return html.Div([
        html.Table(
            [html.Tr([
                html.Td('Device S/N'),
                html.Td(dcc.Input(id='device-sn', type='text', value='')),
                html.Td(html.Button(id='submit-button', n_clicks=0, children='Inspect')),
                html.Td(
                    dcc.Loading([html.Div(id='device-desc',
                                 children=gen_device_status('no device')),
                ])),
                html.Td(html.Div(id='device-desc2', children=''))
            ])]
        ),
        dcc.Tabs(id="tabs", value='', children=[
            dcc.Tab(label='Graph', value='tab-graph',
                style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Config', value='tab-config',
                style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        dcc.Loading([
            html.Div(id='tabs-content')
        ])
    ])

app.layout = serve_layout


@app.callback(Output('device-desc', 'children'),
             [Input('submit-button', 'n_clicks'),
              Input('device-sn', 'n_submit')],
             [State('device-sn', 'value')])
def render_device_content(n_clicks, n_submits, device_sn):
    """Shows device description text when Submit clicked or Enter pressed.
    """
    if (not n_clicks and not n_submits) or not device_sn:
        return gen_device_status('no device')
    df = gen_device_df(device_sn)

    if df.empty:
        applog.debug('Device {} not found'.format(device_sn))
        return gen_device_status('not found')
    else:
        applog.debug('Device {} found'.format(device_sn))
        return gen_device_status('found')


@app.callback([Output('tabs-content', 'children'),
               Output('tabs', 'value')],
              [Input('device-desc', 'children')],
              [State('device-sn', 'value'),
               State('tabs', 'value')])
def render_tabs_content(device_desc, device_sn, tabId):
    """Renders content for *all* tabs when device description updated.
    Content visibility follows selected tab.

    Also select the Logs tab if no selected tab and a device has been 
    selected.
    """
    logsDiv = graph.tab_layout(device_sn, device_desc)
    logsDiv.hidden = (tabId != 'tab-graph')

    configDiv = config.tab_layout(device_sn, device_desc)
    configDiv.hidden = (tabId != 'tab-config')

    if device_desc == DEVICE_NOT_FOUND:
        outputTab = ''
    elif not tabId and device_sn:
        outputTab = 'tab-graph'
    else:
        outputTab = tabId

    return [logsDiv, configDiv], outputTab


@app.callback([Output('graph-div', 'hidden'),
               Output('config-div', 'hidden')],
              [Input('tabs', 'value')])
def render_tab_content(tabId):
    """Shows/Hides tab content when tab clicked"""
    if tabId == 'tab-graph':
        return False, True
    elif tabId == 'tab-config':
        return True, False
    else:
        return True, True
