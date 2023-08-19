from dash import Input, Output, State

import src.common.api_callbacks as api_callbacks
import src.common.component_functions as component_functions

def quarterly_callback(app):
    @app.callback(
        Output('quarterly_table', 'children'),
        Output('quarterly_button', 'loading'),
        Input('quarterly_button', 'n_clicks'),
        State('quarterly_start_year_input', 'value'),
        State('quarterly_end_year_input', 'value'),
        State('bea_quarterly_datasets', 'value'),
        State('fred_quarterly_datasets', 'value'),        
        prevent_initial_call=True
    )
    def request_and_format_quarterly_data(n_clicks, start_year, end_year, selected_bea_tables, selected_fred_tables):
        fred_column_names = {
            'CPIAUCSL': {'value': "CPI"},
            'PAYEMS': {'value': 'Nonfarm Payrolls (Thousands of Persons)'},
            'UNRATE': {'value': 'Unemployment Rate'},
            'USSTHPI': {'value': "House Price Index"}}
        bea_column_names = {
            'T10101': "Real GDP (Quarterly Change)",
            'T10105': "Total GDP (Millions $)",
            'T10107': "GDP (Quarterly Change)",
            'T20100': "Personal Income (Millions $)",
            'T20307': "PCE (Quarterly Change)",
            'T20301': "Real PCE (Quarterly Change)",
            'T20304': "PCEPI"}
        bea_filter_metrics = {
            'T10101': "Gross domestic product",
            'T10105': "Gross domestic product",
            'T10107': "Gross domestic product",
            'T20100': "Personal income",
            'T20307': "Personal consumption expenditures (PCE)",
            'T20301': "Personal consumption expenditures (PCE)",
            'T20304': "Personal consumption expenditures (PCE)"}

        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        fred_api = api_callbacks.DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year, 'lin', 'q', 'sum')
        bea_api = api_callbacks.DataFetcher.fetch_bea_data(selected_bea_tables, all_years_string, 'Q')

        quarterly_request = api_callbacks.DataCleaner(
            time_interval='quarterly',
            fred_api=fred_api,
            fred_column_names=fred_column_names,
            bea_api=bea_api,
            bea_column_names=bea_column_names,
            bea_filter_metrics=bea_filter_metrics
        )
        quarterly_request.process_all_fred_tables(selected_fred_tables)
        quarterly_request.process_all_bea_tables(selected_bea_tables)
        table_df = quarterly_request.merge_dataframes()
        null_report = quarterly_request.generate_null_report(table_df)
        total_nulls_string = f"Total Null Values: {quarterly_request.total_null_count}"
        
        return component_functions.datatable("Quarterly Data", total_nulls_string, null_report, table_df), False
