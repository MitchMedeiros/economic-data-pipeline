from dash_iconify import DashIconify
import dash_mantine_components as dmc

tables_button = dmc.Button(
    "Check Database Tables",
    variant="gradient",
    gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
    className='general-button',
    id='tables_button'
)

tables_select = dmc.Select(
    data=[],
    label="Database Tables",
    searchable=True,
    nothingFound="Table not found",
    className='general-select',
    id='tables_dropdown'
)

table_data_button = dmc.Button(
    "Display Selected Table's Data",
    variant="gradient",
    gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
    className='general-button',
    id='table_data_button'
)
