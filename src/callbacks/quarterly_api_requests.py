from dash import dash_table, html, Input, Output, State
import dash_mantine_components as dmc
import pandas as pd

import src.common.methods_functions as methods_functions

filter_metric = {
    'T10101': "Gross domestic product",
    'T10105': "Gross domestic product",
    'T10107': "Gross domestic product",
    'T20100': "Personal income",
    'T20307': "Personal consumption expenditures (PCE)",
    'T20301': "Personal consumption expenditures (PCE)",
    'T20304': "Personal consumption expenditures (PCE)",
}

bea_column_names = {
    'T10101': "Real GDP (Quarterly Change)",
    'T10105': "Total GDP (Millions $)",
    'T10107': "GDP (Quarterly Change)",
    'T20100': "Personal Income (Millions $)",
    'T20307': "PCE (Quarterly Change)",
    'T20301': "Real PCE (Quarterly Change)",
    'T20304': "PCEPI"
}

fred_column_names = {
    'CPIAUCSL': {'value': "CPI"},
    'PAYEMS': {'value': 'Nonfarm Payrolls (Thousands of Persons)'},
    'UNRATE': {'value': 'Unemployment Rate'}
}

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
        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        bea_api = methods_functions.DataFetcher.fetch_bea_data(selected_bea_tables, all_years_string, 'Q')
        fred_api = methods_functions.DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year, 'q', 'sum')

        all_dfs = []
        for table in selected_fred_tables:
            fred_df = methods_functions.process_fred_table(fred_api, table, fred_column_names, quarterly=True)
            if fred_df is not None: all_dfs.append(fred_df)
        for table in selected_bea_tables:
            bea_df = methods_functions.process_bea_table(bea_api, table, filter_metric, bea_column_names)
            if bea_df is not None: all_dfs.append(bea_df)

        table_df = all_dfs[0]
        for i in range(1, len(all_dfs)):
            table_df = pd.merge(table_df, all_dfs[i], on='date')
        
        return [
            dmc.Text("Quarterly Data", weight=550, size='lg', style={'margin-top': '10px', 'margin-bottom': '10px'}),
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
