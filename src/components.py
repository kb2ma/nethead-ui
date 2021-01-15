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

from app import app, applog, db

import pandas as pd

"""Component display for a device"""

def _gen_component_df(device_id):
    """Generate Pandas dataframe from component query."""
    sql = "SELECT dc.ctype_id, dc.instance_id, datetime(dc.last_update, 'unixepoch') as alias_last_update \
        FROM device_component dc WHERE device_id='{}'"

    df = pd.read_sql(sql.format(device_id), db)
    return df


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
        split_col = col.partition('.')
        if split_col[0] == 'alias':
            col_list.append({'id' : 'alias_{}'.format(split_col[2]),
                             'name' : split_col[2]})
        else:
            col_list.append({'id' : split_col[2], 'name' : split_col[2]})

    return col_list

# invariant, so just create once
columns = _gen_table_cols(['dc.ctype_id', 'dc.instance_id', 'alias.last_update'])

def page_layout(device_id):
    df = _gen_component_df(device_id)
    if not df.empty:
        return [
            html.H5("Components for device " + device_id),
            dash_table.DataTable(id='comp-table', columns=columns,
                                 data=df.to_dict('records'))
        ]
    return 'No components found'
