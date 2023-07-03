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
    def fetch_bea_data(selected_bea_tables, all_years_string, frequency):
        bea_base_url = f"https://apps.bea.gov/api/data/"

        bea_endpoints = {
            table: (f"?&UserID={my_config.BEA_KEY}"
                     "&method=GetData"
                     "&DataSetName=NIPA"
                    f"&Frequency={frequency}"
                    f"&TableName={table}"
                    f"&Year={all_years_string}")
            for table in selected_bea_tables
        }

        bea_api = RestAPI(bea_base_url, bea_endpoints)
        bea_api.fetch_data()
        return bea_api

    @staticmethod
    def fetch_fred_data(selected_fred_tables, start_year, end_year, frequency, aggregation):
        # Monthly data is converted to quarterly data by setting the frequency to 'q' and aggregation method to sum
        fred_units = 'lin'
        fred_frequency = frequency
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
                    f"&aggregation_method={aggregation}"
                     "&file_type=json")
            for table in selected_fred_tables
        }

        fred_api = RestAPI(fred_base_url, fred_endpoints)
        fred_api.fetch_data()
        return fred_api
    
    @staticmethod
    def fetch_treasury_data(selected_treasury_tables, dates):
        treasury_base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"

        treasury_endpoints = {
            f'{table}': f"{table}?&filter=record_fiscal_year:in:({dates})&page[size]=10000" for table in selected_treasury_tables
        }

        treasury_api = RestAPI(treasury_base_url, treasury_endpoints)
        treasury_api.fetch_data()
        return treasury_api

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
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.year.astype(str) + 'Q' + df['date'].dt.quarter.astype(str)
        return df
    except KeyError:
        return dmc.Alert(
            title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
            icon=DashIconify(icon='mingcute:alert-fill'),
            color='yellow',
            withCloseButton=True,
        ), False

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