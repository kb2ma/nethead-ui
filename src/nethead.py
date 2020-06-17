import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Must import server to satisfy Flask even though not used in this module.
from app import app, applog, db, server
import devices

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
    if pathname in ['/', '/devices']:
        return devices.page_layout()
    else:
        return html.P('The pathname {pathname} was not recognised...')

