from dash import dash_table, html, Input, Output, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import pandas as pd
import requests

import my_config

filter_metrics = {
    'T10101': "Gross domestic product",
    'T10105': "Gross domestic product",
    'T10107': "Gross domestic product",
    'T20100': "Personal income"
}

table_names = {
    'T10101': "GDP Quarterly Change",
    'T10105': "GDP Quarterly Change",
    'T10107': "GDP Quarterly Change",
    'T20100': "Personal Income",
    'CPIAUCSL': "CPI Quarterly Change"
}

class RestAPI:
    def __init__(self, base_url, endpoints):
        self.base_url = base_url
        self.endpoints = endpoints
        self.data = {}

    def fetch_data(self):
        for table, endpoint in self.endpoints.items():
            url = self.base_url + endpoint
            response = requests.get(url)
            if response.status_code == 200: self.data[table] = response.json()

class DataFetcher:
    @staticmethod
    def fetch_bea_data(selected_bea_tables, all_years_string):
        bea_base_url = f"https://apps.bea.gov/api/data/"

        bea_endpoints = {
            table: (f"?&UserID={my_config.BEA_KEY}"
                     "&method=GetData"
                     "&DataSetName=NIPA"
                     "&Frequency=Q"
                    f"&TableName={table}"
                    f"&Year={all_years_string}")
            for table in selected_bea_tables
        }

        bea_api = RestAPI(bea_base_url, bea_endpoints)
        bea_api.fetch_data()
        return bea_api

    @staticmethod
    def fetch_fred_data(selected_fred_tables, start_year, end_year):
        # Monthly data is converted to quarterly data by setting the frequency to 'q' and aggregation method to sum
        fred_units = 'pch'
        fred_frequency = 'q'
        fred_start_year = f"{start_year}-01-01"
        fred_end_year = f"{end_year}-01-01"

        fred_base_url = "https://api.stlouisfed.org/fred/series/observations"

        fred_endpoints = {
            table: (f"?series_id={table}"
                    f"&api_key={my_config.FRED_KEY}"
                    f"&observation_start={fred_start_year}"
                    f"&observation_end={fred_end_year}"
                    f"&units={fred_units}"
                    f"&frequency={fred_frequency}"
                     "&aggregation_method=sum"
                     "&file_type=json")
            for table in selected_fred_tables
        }

        fred_api = RestAPI(fred_base_url, fred_endpoints)
        fred_api.fetch_data()
        return fred_api

def process_bea_table(api, table, filter_metrics, table_names):
    try:
        data = api.data[table]['BEAAPI']['Results']['Data']
        df = pd.DataFrame(data, columns=['TimePeriod', 'DataValue', 'METRIC_NAME', 'LineDescription'])
        df = df.loc[df['LineDescription'] == filter_metrics[table]].drop(columns=['LineDescription'])
    except KeyError:
        return dmc.Alert(
            title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
            icon=DashIconify(icon='mingcute:alert-fill'),
            color='yellow',
            withCloseButton=True,
        ), False

    # Pivoting the table to have seperate columns for each distinct calculation method of the general economic metric.
    sliced_dfs = [
        df.loc[df['METRIC_NAME'] == metric]
        .drop(columns=['METRIC_NAME'])
        .reset_index(drop=True)
        .rename(columns={'DataValue': f'{table_names[table]} - ' + metric})
        for metric in df['METRIC_NAME'].unique()
    ]
    pivoted_df = sliced_dfs[0]
    for i in range(1, len(sliced_dfs)):
        pivoted_df = pd.merge(pivoted_df, sliced_dfs[i], on='TimePeriod')
    pivoted_df.rename(columns={'TimePeriod': 'date'}, inplace=True)
    return pivoted_df

def process_fred_table(api, table, table_names):
    try:
        data = api.data[table]['observations']
        df = pd.DataFrame(data, columns=['date', 'value']).rename(columns={'value': table_names[table]})
        return df
    except KeyError:
        return dmc.Alert(
            title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
            icon=DashIconify(icon='mingcute:alert-fill'),
            color='yellow',
            withCloseButton=True,
        ), False

def bea_fred_callback(app):
    @app.callback(
        Output('bea_fred_table', 'children'),
        Output('quarterly_button', 'loading'),
        Input('quarterly_button', 'n_clicks'),
        State('bea_fred_start_year_input', 'value'),
        State('bea_fred_end_year_input', 'value'),
        State('bea_datasets', 'value'),
        State('fred_datasets', 'value'),        
        prevent_initial_call=True
    )
    def request_and_wrangle_data(n_clicks, start_year, end_year, selected_bea_tables, selected_fred_tables):
        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        bea_api = DataFetcher.fetch_bea_data(selected_bea_tables, all_years_string)
        fred_api = DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year)

        all_dfs = []
        for table in selected_bea_tables:
            bea_df = process_bea_table(bea_api, table, filter_metrics, table_names)
            if bea_df is not None: all_dfs.append(bea_df)
        for table in selected_fred_tables:
            fred_df = process_fred_table(fred_api, table, table_names)
            if fred_df is not None: all_dfs.append(fred_df)

        table_df = all_dfs[0]
        for i in range(1, len(all_dfs)):
            table_df = pd.merge(table_df, all_dfs[i], on='date')
        
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
