from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

# Components provided to the About modal in the top bar of the app.
about_modal_children = [
    dcc.Markdown(
        '''
        ### About This App

        ---

        '''
    )
]