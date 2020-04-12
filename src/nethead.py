import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app
from app import server
from app import applog

from datetime import datetime
import json
import numpy as np
import pandas as pd
import plotly.express as px
import requests

"""Main/Top view for NetHead UI.
"""

def serve_layout():
    df = _collect_data()
    fig = px.line(df, x="time", y="temp")

    return html.Div([
        dcc.Graph(figure=fig),

        #dash_table.DataTable(id='data-table', 
        #    columns=[{"name": i, "id": i} for i in df.columns],
        #    data=df.to_dict("rows")
        #)
    ])

def _collect_data():
    """Collects data from Graphite into a dataframe.
    """
    url = 'http://localhost:8089/render'
    #url = 'http://[2601:18e:c501:6670:1bae:909f:de25:9a2e]:8089/render'

    params = {
        'target': 'temp.3303.0',
        'from': 'now-6hr',
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

# uses the function to dynamically rebuild page on refresh
app.layout = serve_layout
