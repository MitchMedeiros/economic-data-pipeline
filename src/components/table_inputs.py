from dash_iconify import DashIconify
import dash_mantine_components as dmc

tables_button = dmc.Button(
    "Check Database Tables",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    # gradient={'from': 'rgba(255, 117, 165, .6)', 'to': 'rgba(245, 134, 255, .6)', 'deg': 45},
    style={'margin-top': '5px', 'margin-bottom': '10px'},
    id='tables_button'
)

tables_select = dmc.Select(
    data=[],
    label="Database Tables",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Table not found",
    style={'text-align': 'center'},
    id='tables_dropdown'
)