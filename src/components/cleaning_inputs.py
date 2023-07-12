import dash_mantine_components as dmc

table_select = dmc.Select(
    data=[
        {'label': 'Daily Data', 'value': 'daily'},
        {'label': 'Monthly Data', 'value': 'monthly'},
        {'label': 'Quarterly Data', 'value': 'quarterly'}
    ],
    value='daily',
    label="Data",
    searchable=True,
    nothingFound="Table not found",
    style={'text-align': 'center', 'width': '250px'},
    id='table_select'
)

null_checkbox = dmc.Checkbox(
    label="Null Values",
    checked=False,
    style={'margin-top': '10px', 'margin-bottom': '15px'},
    id="null_checkbox"
)

duplicates_checkbox = dmc.Checkbox(
    label="Duplicate Rows",
    checked=False,
    style={'margin-top': '10px', 'margin-bottom': '15px'},
    id="duplicates_checkbox"
)

clean_button = dmc.Button(
    "Clean the Data",
    variant="gradient",
    gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
    className='general-button',
    id='clean_button'
)

save_button = dmc.Button(
    "Save to Database",
    variant="gradient",
    gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
    className='general-button',
    id='save_button'
)
