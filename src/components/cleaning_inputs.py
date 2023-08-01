import src.common.component_functions as component_functions

table_select = component_functions.select(
    [
        {'label': 'Daily Data', 'value': 'daily'},
        {'label': 'Monthly Data', 'value': 'monthly'},
        {'label': 'Quarterly Data', 'value': 'quarterly'}
    ],
    'daily',
    "Data",
    'table_select'
)

null_checkbox = component_functions.checkbox("Null Values", "null_checkbox")

duplicates_checkbox = component_functions.checkbox("Duplicate Rows", "duplicates_checkbox")

null_select = component_functions.select(
    [
        {'label': 'remove the row', 'value': 'none'},
        {'label': 'average the two adjacent values', 'value': 'two'},
        {'label': 'average the four adjacent values', 'value': 'four'}
    ],
    'two',
    "How to Handle Null Values",
    'null_select'
)

clean_button = component_functions.button(
    "Clean the Data",
    'clean_button',
    component_functions.icon('mdi:database-edit-outline')
)

save_button = component_functions.button(
    "Save to Database",
    'save_button',
    component_functions.icon('majesticons:data-plus-line')
)
