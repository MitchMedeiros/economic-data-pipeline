import src.common.component_functions as component_functions

tables_button = component_functions.button("Check Database Tables", 'tables_button')

tables_select = component_functions.select(
    [],
    None,
    "Database Tables",
    'tables_dropdown'
)

table_data_button = component_functions.button("Display Selected Table's Data", 'table_data_button')
