import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from app import app, applog, db

import pandas as pd

"""Device list display"""

def _gen_registration_df():
    """Generate Pandas dataframe from registration rows."""
    sql = "SELECT r.reg_id, r.endpoint, r.identity, r.lifetime, r.links \
        FROM registration r"

    df = pd.read_sql(sql, db)
    return df


def _gen_table_cols(colList):
    """Generate Dash table columns in the expected format.

    :param colList: list of columns; must be in format <table-alias.name>,
                    like "s.serial_number"
    """
    return [{'id' : col, 'name' : col} for col in colList]


def page_layout():
    df = _gen_registration_df()
    if not df.empty:
        return [
            dash_table.DataTable(id='reg-table',
                columns=_gen_table_cols(['reg_id', 'endpoint', 'identity', 'lifetime', 'links']),
                data=(df.to_dict('records'))
        )]
    else:
        return 'No devices found'
