import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app
from app import server
from app import applog

import json
import numpy as np
import pandas as pd
import requests

"""Main/Top view for NetHead UI.
"""

def serve_layout():
    return html.Div([
        dash_table.DataTable(id='data-table', 
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("rows")
        )
    ])

def _collect_data():
    """Collects data from Graphite.
    """
    url = 'http://localhost:8089/render'
    params = {
        'target': 'time.3303.0',
        'from': 'now-30min',
        'format': 'json'
    }

    data = json.loads(requests.get(url, params=params).text)
    #print(data)
    series = np.array(data[0]['datapoints'])
    #print(series)
    #print(series[:, 0])
    #print(series[:, 1])

    return pd.DataFrame(series,
                        index=series[:, 1],
                        columns=['temp', 'time'])


df = _collect_data()
#print(df)

app.layout = serve_layout
