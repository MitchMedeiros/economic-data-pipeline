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
    className='general-select',
    id='table_select'
)

null_checkbox = dmc.Checkbox(
    label="Null Values",
    checked=False,
    className='general-checkbox',
    id="null_checkbox"
)

duplicates_checkbox = dmc.Checkbox(
    label="Duplicate Rows",
    checked=False,
    className='general-checkbox',
    id="duplicates_checkbox"
)

null_select = dmc.Select(
    data=[
        {'label': 'remove the row', 'value': 'none'},
        {'label': 'average the two adjacent values', 'value': 'two'},
        {'label': 'average the four adjacent values', 'value': 'four'}
    ],
    value='two',
    label="How to Handle Null Values",
    searchable=True,
    nothingFound="Method not found",
    className='general-select',
    id='null_select'
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
