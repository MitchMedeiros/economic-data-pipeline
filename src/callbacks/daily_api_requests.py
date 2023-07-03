from dash import dash_table, html, Input, Output, State
import dash_mantine_components as dmc
import pandas as pd

import src.common.methods_functions as methods_functions

table_columns = {
    'v1/accounting/dts/dts_table_1': ['record_date', 'close_today_bal', 'account_type'],
    'v2/accounting/od/debt_to_penny': ['record_date', 'tot_pub_debt_out_amt']
}

table_column_names = {
    'v1/accounting/dts/dts_table_1': {'close_today_bal': 'Daily Treasury Balance (M $)'},
    'v2/accounting/od/debt_to_penny': {'tot_pub_debt_out_amt': 'Outstanding US Debt ($)'}
}

def daily_callback(app):
    @app.callback(
        Output('daily_table', 'children'),
        Output('daily_button', 'loading'),
        Input('daily_button', 'n_clicks'),
        State('daily_start_year_input', 'value'),
        State('daily_end_year_input', 'value'),        
        State('treasury_daily_datasets', 'value'),   
        prevent_initial_call=True
    )
    def request_and_format_daily_data(n_clicks, start_year, end_year, selected_treasury_tables):
        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        treasury_api = methods_functions.DataFetcher.fetch_treasury_data(selected_treasury_tables, all_years_string)

        all_dfs = []
        for table in selected_treasury_tables:
            treasury_df = methods_functions.process_treasury_table(treasury_api, table, table_columns, table_column_names)
            if treasury_df is not None: all_dfs.append(treasury_df)

        table_df = all_dfs[0]
        for i in range(1, len(all_dfs)):
            table_df = pd.merge(table_df, all_dfs[i], on='record_date')

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
                    id='upload_table'
                )
            )
        ], False
