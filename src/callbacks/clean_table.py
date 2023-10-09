from dash import Input, Output, State

import src.common.api_callbacks as api_callbacks
import src.common.component_functions as component_functions

def table_cleaning_callback(app):
    @app.callback(
        Output('clean_table_div', 'children'),
        Input('clean_button', 'n_clicks'),
        State('table_select', 'value'),
        State('null_checkbox', 'value'),
        State('duplicates_checkbox', 'value'),
        State('null_select', 'value'),
        State('daily_table', 'children'),
        State('monthly_table', 'children'),
        State('quarterly_table', 'children'),
        prevent_initial_call=True
    )
    def clean_data(n_clicks, data_select, null_checkbox, duplicate_checkbox, null_dropdown, daily_data, monthly_data, quarterly_data):
        if data_select == 'daily':
            print(daily_data)