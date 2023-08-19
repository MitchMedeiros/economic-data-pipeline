from dash import Input, Output, State

import src.common.api_callbacks as api_callbacks
import src.common.component_functions as component_functions

def daily_callback(app):
    @app.callback(
        Output('daily_table', 'children'),
        Output('daily_button', 'loading'),
        Input('daily_button', 'n_clicks'),
        State('daily_start_year_input', 'value'),
        State('daily_end_year_input', 'value'),
        State('fred_daily_datasets', 'value'),   
        State('treasury_daily_datasets', 'value'),
        prevent_initial_call=True
    )
    def request_and_format_daily_data(n_clicks, start_year, end_year, selected_fred_tables, selected_treasury_tables):
        fred_column_names = {
            'SP500': {'value': "S&P 500 Value ($)"},
            'NASDAQCOM': {'value': "Nasdaq Composite Value ($)"}}
        treasury_column_names = {
            'v1/accounting/dts/dts_table_1': {'record_date': 'date', 'close_today_bal': 'Daily Treasury Balance (Millions $)'},
            'v2/accounting/od/debt_to_penny': {'record_date': 'date', 'tot_pub_debt_out_amt': 'Outstanding US Debt ($)'}}
        treasury_columns = {
            'v1/accounting/dts/dts_table_1': ['record_date', 'close_today_bal', 'account_type'],
            'v2/accounting/od/debt_to_penny': ['record_date', 'tot_pub_debt_out_amt']}

        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        fred_api = api_callbacks.DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year, 'lin', 'd', 'lin')
        treasury_api = api_callbacks.DataFetcher.fetch_treasury_data(selected_treasury_tables, all_years_string)

        daily_request = api_callbacks.DataCleaner(
            time_interval='daily',
            fred_api=fred_api,
            fred_column_names=fred_column_names,
            treasury_api=treasury_api,
            treasury_column_names=treasury_column_names,
            treasury_columns=treasury_columns
        )
        daily_request.process_all_fred_tables(selected_fred_tables)
        daily_request.process_all_treasury_tables(selected_treasury_tables)
        table_df = daily_request.merge_dataframes()
        null_report = daily_request.generate_null_report(table_df)
        total_nulls_string = f"Total Null Values: {daily_request.total_null_count}"
        
        return component_functions.datatable("Daily Data", total_nulls_string, null_report, table_df), False
