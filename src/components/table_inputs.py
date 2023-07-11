from dash_iconify import DashIconify
import dash_mantine_components as dmc

tables_button = dmc.Button(
    "Check Database Tables",
    variant="gradient",
    gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
    style={'margin-top': '5px', 'margin-bottom': '10px'},
    id='tables_button'
)

tables_select = dmc.Select(
    data=[],
    label="Database Tables",
    searchable=True,
    nothingFound="Table not found",
    style={'text-align': 'center'},
    id='tables_dropdown'
)
