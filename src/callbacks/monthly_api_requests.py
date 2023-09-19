from dash import Input, Output, State

import src.common.api_callbacks as api_callbacks
import src.common.component_functions as component_functions

def monthly_callback(app):
    @app.callback(
        Output('monthly_table', 'children'),
        Output('monthly_button', 'loading'),
        Input('monthly_button', 'n_clicks'),
        State('monthly_start_year_input', 'value'),
        State('monthly_end_year_input', 'value'),
        State('fred_monthly_datasets', 'value'),
        State('bea_monthly_datasets', 'value'),
        prevent_initial_call=True
    )
    def request_and_format_monthly_data(n_clicks, start_year, end_year, selected_fred_tables, selected_bea_tables):
        fred_column_names = {
            'CPIAUCSL': {'value': "CPI"},
            'PAYEMS': {'value': 'Nonfarm Payrolls (Thousands of Persons)'},
            'UNRATE': {'value': 'Unemployment Rate'},
            'CSUSHPINSA': {'value': "Case-Shiller U.S. Home Price Index"}}
        bea_column_names = {
            'T20600': 'Personal Income (Millions $)',
            'T20807': 'PCE (Monthly Change)',
            'T20801': 'Real PCE (Monthly Change)',
            'T20804': "PCEPI"}
        bea_filter_metrics = {
            'T20600': "Personal income",
            'T20807': "Personal consumption expenditures (PCE)",
            'T20801': "Personal consumption expenditures (PCE)",
            'T20804': "Personal consumption expenditures (PCE)"}

        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        fred_api = api_callbacks.DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year, 'lin', 'm', 'avg')
        bea_api = api_callbacks.DataFetcher.fetch_bea_data(selected_bea_tables, all_years_string, 'M')

        monthly_request = api_callbacks.DataCleaner(time_interval='monthly')
        monthly_request.process_fred_tables(selected_fred_tables, fred_api, fred_column_names)
        monthly_request.process_bea_tables(selected_bea_tables, bea_api, bea_column_names, bea_filter_metrics)
        table_df = monthly_request.merge_dataframes()
        null_report = monthly_request.generate_null_report(table_df)
        total_nulls_string = f"Total Null Values: {monthly_request.total_null_count}"
        
        return component_functions.datatable("Monthly Data", total_nulls_string, null_report, table_df), False
