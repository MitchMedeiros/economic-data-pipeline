from dash import dash_table, html, Input, Output, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import pandas as pd

from . bea_fred_api import RestAPI

table_columns = {
    'v1/accounting/dts/dts_table_1': ['record_date', 'close_today_bal', 'account_type'],
    'v2/accounting/od/debt_to_penny': ['record_date', 'tot_pub_debt_out_amt']
}

table_column_names = {
    'v1/accounting/dts/dts_table_1': {'close_today_bal': 'Daily Treasury Balance (M $)'},
    'v2/accounting/od/debt_to_penny': {'tot_pub_debt_out_amt': 'Outstanding US Debt ($)'}
}

class DataFetcher:
    @staticmethod
    def fetch_treasury_data(selected_treasury_tables, dates):
        treasury_base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"

        treasury_endpoints = {
            f'{table}': f"{table}?&filter=record_fiscal_year:in:({dates})&page[size]=10000" for table in selected_treasury_tables
        }

        treasury_api = RestAPI(treasury_base_url, treasury_endpoints)
        treasury_api.fetch_data()
        return treasury_api
    
def process_treasury_table(api, table, table_columns, table_column_names):
    try:
        data = api.data[table]['data']
        df = pd.DataFrame(data, columns=table_columns[table]).rename(columns=table_column_names[table])

        if table == 'v1/accounting/dts/dts_table_1':
            df = df.loc[df['account_type'] == 'Federal Reserve Account'].drop(columns=['account_type']).reset_index(drop=True)
    except KeyError:
        return dmc.Alert(
            title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
            icon=DashIconify(icon='mingcute:alert-fill'),
            color='yellow',
            withCloseButton=True,
        ), False
    return df

def treasury_callback(app):
    @app.callback(
        Output('daily_table', 'children'),
        Output('daily_button', 'loading'),
        Input('daily_button', 'n_clicks'),
        State('daily_start_year_input', 'value'),
        State('daily_end_year_input', 'value'),        
        State('treasury_daily_datasets', 'value'),   
        prevent_initial_call=True
    )
    def get_bea_data(n_clicks, start_year, end_year, selected_treasury_tables):
        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        treasury_api = DataFetcher.fetch_treasury_data(selected_treasury_tables, all_years_string)

        all_dfs = []
        for table in selected_treasury_tables:
            treasury_df = process_treasury_table(treasury_api, table, table_columns, table_column_names)
            if treasury_df is not None: all_dfs.append(treasury_df)

        table_df = all_dfs[0]
        for i in range(1, len(all_dfs)):
            table_df = pd.merge(table_df, all_dfs[i], on='record_date')

        return html.Div(
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
        ), False
