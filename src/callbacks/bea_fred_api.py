from dash import dash_table, html, Input, Output, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import pandas as pd
import requests

import my_config

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
        fred_units = "pch"
        fred_frequency = "q"
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

def add_date_table(table, dataset_list):
    date_table_added = table not in dataset_list
    if date_table_added: dataset_list += [table]
    return date_table_added

def create_date_series(date_name, data):
    periods = [item[date_name] for item in data]
    unique_periods = list(set(periods))
    date_sr = pd.Series(unique_periods, name='date').sort_values().reset_index(drop=True)
    return date_sr

def process_bea_table(api, table, filter_metrics, table_names):
    try:
        data = api.data[table]['BEAAPI']['Results']['Data']
        df = pd.DataFrame(data, columns=['DataValue', 'METRIC_NAME', 'LineDescription'])
    except KeyError:
        return dmc.Alert(
            title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
            icon=DashIconify(icon='mingcute:alert-fill'),
            color='yellow',
            withCloseButton=True,
        ), False

    # Filtering the table to only include the general economic metric that we want i.e. GDP or GDI
    if table != 'T20307':
        df = df.loc[df['LineDescription'] == filter_metrics[table]].drop(columns=['LineDescription'])

    # Pivoting the table to have seperate columns for each distinct calculation method of the general economic metric.
    sliced_dfs = [
        df.loc[df['METRIC_NAME'] == metric]
        .drop(columns=['METRIC_NAME'])
        .reset_index(drop=True)
        .rename(columns={'DataValue': f'{table_names[table]} - ' + metric})
        for metric in df['METRIC_NAME'].unique()
    ]
    pivoted_df = pd.concat(sliced_dfs, axis=1)
    return pivoted_df

def process_fred_table(api, table, table_names):
    try:
        data = api.data[table]['observations']
        df = pd.DataFrame(data, columns=['value']).rename(columns={'value': table_names[table]})
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
        State('start_year_input', 'value'),
        State('end_year_input', 'value'),
        State('bea_datasets', 'value'),
        State('fred_datasets', 'value'),        
        prevent_initial_call=True
    )
    def request_and_wrangle_data(n_clicks, start_year, end_year, selected_bea_tables, selected_fred_tables):
        all_years_string = ','.join(str(year) for year in range(start_year, end_year + 1))

        date_table_added = add_date_table('T10101', selected_bea_tables)

        # In general, each table contains multiple economic metrics, i.e. GDP and GNP.
        # This dictionary is used to filter on the metric we're interested in per table.
        filter_metrics = {
            "T10101": "Gross domestic product",
            'T10105': "Gross domestic product",
            'T10107': "Gross domestic product",
            'T20100': "Personal income"
        }

        table_names = {
            "T10101": "GDP Quarterly Change",
            'T10105': "GDP Quarterly Change",
            'T10107': "GDP Quarterly Change",
            'T20100': "Personal Income",
            'CPIAUCSL': "CPI Quarterly Change"
        }

        bea_api = DataFetcher.fetch_bea_data(selected_bea_tables, all_years_string)
        fred_api = DataFetcher.fetch_fred_data(selected_fred_tables, start_year, end_year)
        date_sr = create_date_series('TimePeriod', bea_api.data['T10101']['BEAAPI']['Results']['Data'])

        if date_table_added: selected_bea_tables.remove('T10101')

        all_dfs = [date_sr]

        for table in selected_bea_tables:
            bea_df = process_bea_table(bea_api, table, filter_metrics, table_names)
            if bea_df is not None: all_dfs.append(bea_df)

        for table in selected_fred_tables:
            fred_df = process_fred_table(fred_api, table, table_names)
            if fred_df is not None: all_dfs.append(fred_df)

        table_df = pd.concat(all_dfs , axis=1)
        
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
