import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from app import applog

from datetime import datetime
import json
import numpy as np
import pandas as pd
import plotly.express as px
import requests

"""Displays graph of time series data from Graphite.

Refreshes graph once a minute.
"""

def _collect_data():
    """Collects data from Graphite into a dataframe.
    """
    url = 'http://localhost:8089/render'
    #url = 'http://[2601:18e:c501:6670:1bae:909f:de25:9a2e]:8089/render'

    params = {
        'target': 'temp.3303.0',
        'from': 'now-6h',
        'format': 'json'
    }

    data = json.loads(requests.get(url, params=params).text)
    series = np.array(data[0]['datapoints'])

    df = pd.DataFrame(series,
                        index=series[:, 1],
                        columns=['temp', 'time'])
    # time as hours:minutes
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x).strftime('%H:%M'))
    return df


def tab_layout(deviceSn, device_desc):
    global graph;
    if deviceSn and device_desc == 'Status: found':
        df = _collect_data()
        fig = px.line(df, x="time", y="temp")

        return html.Div(id='graph-div', children=[
            dcc.Graph(id='graph-ref', figure=fig, style={'height': '500px'}),
            dcc.Interval(
                id='graph-refresh',
                interval=60*1000, # in milliseconds
                n_intervals=0)
            ])
    else:
        return html.Div(id='graph-div', children=[ 'No valid device' ])


@app.callback(Output('graph-ref', 'figure'),
              [Input('graph-refresh', 'n_intervals')])
def updateGraph(n):
    df = _collect_data()
    applog.debug("Refreshing graph")
    return px.line(df, x="time", y="temp")

