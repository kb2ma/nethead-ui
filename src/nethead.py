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
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Must import server to satisfy Flask even though not used in this module.
from app import app, applog, db, server
import devices, components

"""Main/Top view for NetHead UI."""

app.layout = html.Div([
        dcc.Location(id='url'),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink('Devices', href='/devices', id='devices-link'),
            ],
            brand='Nethead',
            brand_style={'font-size': '12pt'},
            color='primary',
            dark=True,
        ),
        dbc.Container(id='page-content', className='pt-4'),
    ])

@app.callback(Output('devices-link', 'active'),
             [Input('url', 'pathname')]
)
def toggle_active_links(pathname):
    """Sets active state of Nav links"""
    if pathname == '/':
        return True
    return True


@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')]
)
def render_page(pathname):
    if not pathname or (pathname in ['/', '/devices']):
        return devices.page_layout()
    elif pathname.startswith('/components'):
        segments = pathname.rsplit('/')
        if len(segments) == 3:
            return components.page_layout(segments[2])

    return html.P('The pathname {} was not recognised...'.format(pathname))

