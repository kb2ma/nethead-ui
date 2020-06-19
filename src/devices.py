import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from app import app, applog, db

import pandas as pd

"""Device list display"""

def _gen_registration_df():
    """Generate Pandas dataframe from registration query."""
    sql = "SELECT r.reg_id, r.endpoint, r.identity, r.lifetime, datetime(r.last_update, 'unixepoch') as alias_last_update \
        FROM registration r"

    df = pd.read_sql(sql, db)
    return df


def _gen_table_cols(col_ids):
    """Generate Dash table columns in the expected format.

    :param col_ids: list of columns; must be in format <table-alias.name>,
                    like "s.serial_number", as in the SQL select statement
                    -- except for derived column values which must literally
                    use "alias." plus the name.
    :return: List of dictionaries, where ach contains an 'id' and a 'name' key
             for a Dash DataTable.
    """
    col_list = []
    for col in col_ids:
        split_col = col.partition('.')
        if split_col[0] == 'alias':
            col_list.append({'id' : 'alias_{}'.format(split_col[2]), 'name' : split_col[2]})
        else:
            col_list.append({'id' : split_col[2], 'name' : split_col[2]})

    return col_list


def page_layout():
    df = _gen_registration_df()
    if not df.empty:
        return [
            dash_table.DataTable(id='reg-table',
                columns=_gen_table_cols(['r.endpoint', 'r.reg_id', 'r.identity', 'r.lifetime', 'alias.last_update']),
                data=(df.to_dict('records'))
        )]
    return 'No devices found'
