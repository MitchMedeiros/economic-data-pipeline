from dash import dash_table, html, Input, Output, State
import dash_mantine_components as dmc
import pandas as pd

import src.common.methods_functions as methods_functions

treasury_columns = {
    'v1/accounting/dts/dts_table_1': ['record_date', 'close_today_bal', 'account_type'],
    'v2/accounting/od/debt_to_penny': ['record_date', 'tot_pub_debt_out_amt']
}

fred_column_names = {
    'SP500': {'value': "S&P 500 Value ($)"},
    'NASDAQCOM': {'value': "Nasdaq Composite Value ($)"}
}

treasury_column_names = {
    'v1/accounting/dts/dts_table_1': {'record_date': 'date', 'close_today_bal': 'Daily Treasury Balance (Millions $)'},
    'v2/accounting/od/debt_to_penny': {'record_date': 'date', 'tot_pub_debt_out_amt': 'Outstanding US Debt ($)'}
}

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
        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        fred_api = methods_functions.DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year, 'lin', 'd', 'lin')
        treasury_api = methods_functions.DataFetcher.fetch_treasury_data(selected_treasury_tables, all_years_string)

        all_dfs = []
        for table in selected_fred_tables:
            fred_df = methods_functions.process_fred_table(fred_api, table, fred_column_names)
            if fred_df is not None: all_dfs.append(fred_df)
        for table in selected_treasury_tables:
            treasury_df = methods_functions.process_treasury_table(treasury_api, table, treasury_columns, treasury_column_names)
            if treasury_df is not None: all_dfs.append(treasury_df)

        table_df = all_dfs[0]
        for i in range(1, len(all_dfs)):
            table_df = pd.merge(table_df, all_dfs[i], on='date')

        return [
            dmc.Text("Daily Data", weight=550, size='lg', style={'margin-bottom': '10px'}),
            html.Div(
                dash_table.DataTable(
                    data=table_df.to_dict('records'),
                    columns=[{'name': str(i), 'id': str(i)} for i in table_df.columns],
                    fill_width=False,
                    cell_selectable=False,
                    style_as_list_view=True,
                    style_header={
                        'color': 'rgba(220, 220, 220, 0.95)',
                        'padding': '10px',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    },
                    style_data={'color': 'rgba(220, 220, 220, 0.85)'},
                    style_cell={'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'},
                    style_cell_conditional=[{'textAlign': 'center'}],
                    id='daily_dash_table'
                )
            )
        ], False
