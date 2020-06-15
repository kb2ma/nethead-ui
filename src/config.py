import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app
from app import applog
from app import db

import pandas as pd

"""
Configuration display for a device.
"""

def _gen_registration_df(device_sn):
    """Generate Pandas dataframe from registration row for a device."""
    rawSql = "SELECT r.reg_id, r.endpoint, r.identity, r.lifetime, r.links \
        FROM registration r \
        WHERE r.endpoint = '{}'"
    sql = rawSql.format(device_sn)

    df = pd.read_sql(sql, db)
    return df


def _gen_table_cols(colList):
    """Generate Dash table columns in the expected format.

    :param colList: list of columns; must be in format <table-alias.name>,
                    like "s.serial_number"
    """
    return [{'id' : col, 'name' : col} for col in colList]


def tab_layout(device_sn, device_desc):
    applog.debug('device_sn {}, device_desc {}'.format(device_sn, device_desc))
    if device_sn and (device_desc == 'Status: found'):
        df = _gen_registration_df(device_sn)
        applog.debug('reg df {}'.format(df))
        return html.Div(id='config-div', children=[
            html.H5("Registration"),
            dash_table.DataTable(id='reg-table',
                columns=_gen_table_cols(['reg_id', 'endpoint', 'identity', 'lifetime', 'links']),
                data=(_gen_registration_df(device_sn).to_dict('records'))
            )
        ])
    else:
        return html.Div(id='config-div', children=[ 'No valid device' ])
