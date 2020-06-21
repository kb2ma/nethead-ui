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
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app, applog, db

import pandas as pd

"""Device list display; automatic refresh"""

def _gen_registration_df():
    """Generate Pandas dataframe from registration query."""
    sql = "SELECT r.reg_id, r.endpoint, r.identity, r.lifetime, datetime(r.last_update, 'unixepoch') as alias_last_update \
        FROM registration r"

    return pd.read_sql(sql, db)


def _gen_table_cols(col_ids):
    """Generate Dash table columns in the expected format.

    :param col_ids: list of columns; must be in format <table-alias.name>,
                    like "s.serial_number", as in the SQL select statement
                    -- except for derived column values which must literally
                    use "alias." plus the name.
    :return: List of dictionaries, where each contains an 'id' and a 'name' key
             for a Dash DataTable.
    """
    col_list = []
    for col in col_ids:
        col_dict = {}

        split_col = col.partition('.')
        if split_col[0] == 'alias':
            col_dict['id'] = 'alias_{}'.format(split_col[2])
        else:
            col_dict['id'] = split_col[2]
        col_dict['name'] = split_col[2]

        col_list.append(col_dict)

    return col_list

# invariant, so just create once
columns = _gen_table_cols(['r.endpoint', 'r.reg_id', 'r.identity', 'r.lifetime',
                           'alias.last_update'])

def page_layout():
    df = _gen_registration_df()
    if not df.empty:
        return [
            dcc.Location(id='devices-url'),
            html.H5("Devices"),
            dash_table.DataTable(id='reg-table', columns=columns,
                                 data=df.to_dict('records'),
                                 row_selectable='single'),
            dcc.Interval(
                id='reg-refresh',
                interval=60*1000, # in milliseconds
                n_intervals=0)
        ]
    return 'No devices found'


@app.callback(Output('reg-table', 'data'),
              [Input('reg-refresh', 'n_intervals')])
def updateTable(n):
    df = _gen_registration_df()
    if not df.empty:
        return df.to_dict('records')
    else:
        raise PreventUpdate


@app.callback(Output('devices-url', 'pathname'),
             [Input('reg-table', 'selected_rows')])
def viewComponents(selectedRows):
    if selectedRows:
        return '/components/1574'
