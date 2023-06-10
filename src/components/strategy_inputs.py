from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

run_backtest_button = dmc.Button(
    "Request Data",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="lightGreen", width=30),
    variant="gradient",
    n_clicks=0,
    style={'margin-top': '15px'},
    id='run_button'
)