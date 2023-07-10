from dash_iconify import DashIconify
import dash_mantine_components as dmc

null_checkbox = dmc.Checkbox(
    label="Null Values",
    checked=False,
    style={'margin-top': '5px', 'margin-bottom': '10px'},
    id="null_checkbox"
)

duplicates_checkbox = dmc.Checkbox(
    label="Duplicate Rows",
    checked=False,
    style={'margin-top': '5px', 'margin-bottom': '10px'},
    id="duplicates_checkbox"
)

clean_button = dmc.Button(
    "Clean the Data",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    # gradient={'from': 'rgba(255, 117, 165, .6)', 'to': 'rgba(245, 134, 255, .6)', 'deg': 45},
    style={'margin-top': '5px', 'margin-bottom': '10px'},
    id='clean_button'
)
