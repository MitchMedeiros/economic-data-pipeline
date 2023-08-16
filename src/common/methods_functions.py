from dash_iconify import DashIconify
import dash_mantine_components as dmc
import numpy as np
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
            if response.status_code == 200: 
                self.data[table] = response.json()

class DataFetcher:
    @staticmethod
    def fetch_bea_data(selected_bea_tables, all_years_string, frequency):
        bea_base_url = "https://apps.bea.gov/api/data/"

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
    def fetch_fred_data(selected_fred_tables, start_year, end_year, unit, frequency, aggregation):
        # Monthly data is converted to quarterly data by setting the frequency to 'q' and aggregation method to sum
        fred_start_year = f"{start_year}-01-01"
        fred_end_year = f"{end_year}-01-01"

        fred_base_url = "https://api.stlouisfed.org/fred/series/observations"

        fred_endpoints = {
            table: (f"?series_id={table}"
                    f"&api_key={my_config.FRED_KEY}"
                    f"&observation_start={fred_start_year}"
                    f"&observation_end={fred_end_year}"
                    f"&units={unit}"
                    f"&frequency={frequency}"
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
            table: f"{table}?&filter=record_fiscal_year:in:({dates})&page[size]=10000" for table in selected_treasury_tables
        }

        treasury_api = RestAPI(treasury_base_url, treasury_endpoints)
        treasury_api.fetch_data()
        return treasury_api
    
def process_bea_table(api, table, filter_metrics, table_names, monthly=False):
    try:
        data = api.data[table]['BEAAPI']['Results']['Data']
        df = pd.DataFrame(data, columns=['TimePeriod', 'DataValue', 'METRIC_NAME', 'LineDescription'])
        df = df.loc[df['LineDescription'] == filter_metrics[table]].drop(columns=['LineDescription'])

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

        if monthly:
                pivoted_df['date'] = pd.to_datetime(pivoted_df['date'], format='%YM%m').dt.to_period('M')
        return pivoted_df
    except KeyError:
        return dmc.Alert(
            title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
            icon=DashIconify(icon='mingcute:alert-fill'),
            color='yellow',
            withCloseButton=True,
        ), False

# def process_fred_table(api, table, column_names, monthly=False, quarterly=False):
#     try:
#         data = api.data[table]['observations']
#         df = pd.DataFrame(data, columns=['date', 'value']).rename(columns=column_names[table])
#         if monthly:
#             df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
#         if quarterly:
#             df['date'] = pd.to_datetime(df['date'])
#             df['date'] = df['date'].dt.year.astype(str) + 'Q' + df['date'].dt.quarter.astype(str)
#         return df
#     except KeyError:
#         return dmc.Alert(
#             title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
#             icon=DashIconify(icon='mingcute:alert-fill'),
#             color='yellow',
#             withCloseButton=True,
#         ), False

# def process_treasury_table(api, table, table_columns, column_names):
#     try:
#         data = api.data[table]['data']
#         df = pd.DataFrame(data, columns=table_columns[table]).rename(columns=column_names[table])

#         if table == 'v1/accounting/dts/dts_table_1':
#             df = df.loc[df['account_type'] == 'Federal Reserve Account'].drop(columns=['account_type']).reset_index(drop=True)
#     except KeyError:
#         return dmc.Alert(
#             title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
#             icon=DashIconify(icon='mingcute:alert-fill'),
#             color='yellow',
#             withCloseButton=True,
#         ), False
#     return df

def format_and_count_nulls(df):
    df = df.replace('.', np.nan)
    col_names = df.isnull().sum().index
    col_null_values = df.isnull().sum()
    null_list = []
    for i in range(len(col_names)):
        if col_null_values[i] > 0:
            null_list.append(f"{col_names[i]}: {col_null_values[i]}")
    
    total_nulls_string = f"Total Null Values: {df.isnull().sum().sum()}"
    individual_nulls_string = ' | '.join(str(nulls) for nulls in null_list)

    if len(null_list) > 0:
        individual_nulls_string = "Columns with Null Values: " + individual_nulls_string

class DataCleaner:
    def __init__(self, fred_api=None, treasury_api=None, bea_api=None, fred_column_names=None,
                 treasury_column_names=None, bea_column_names=None, bea_filter_metrics=None):
        self.fred_api = fred_api
        self.treasury_api = treasury_api
        self.bea_api = bea_api
        self.fred_column_names = fred_column_names
        self.treasury_column_names = treasury_column_names
        self.bea_column_names = bea_column_names
        self.bea_filter_metrics = bea_filter_metrics
        self.all_dfs = []

    def process_fred_table(self, table, column_names, interval='daily'):
        try:
            data = self.fred_api.data[table]['observations']
            df = pd.DataFrame(data, columns=['date', 'value']).rename(columns=column_names[table])
            if interval == 'daily':
                pass
            if interval == 'monthly':
                df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
            if interval == 'quarterly':
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

    def process_treasury_table(self, table, treasury_columns):
        try:
            data = self.treasury_api.data[table]['data']
            df = pd.DataFrame(data, columns=treasury_columns[table]).rename(columns=self.treasury_column_names[table])

            if table == 'v1/accounting/dts/dts_table_1':
                df = df.loc[df['account_type'] == 'Federal Reserve Account'].drop(columns=['account_type']).reset_index(drop=True)
            return df
        except KeyError:
            return dmc.Alert(
                title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                icon=DashIconify(icon='mingcute:alert-fill'),
                color='yellow',
                withCloseButton=True,
            ), False

    def process_treasury_table(self, table, treasury_columns):
        try:
            data = self.treasury_api.data[table]['data']
            df = pd.DataFrame(data, columns=treasury_columns[table]).rename(columns=self.treasury_column_names[table])

            if table == 'v1/accounting/dts/dts_table_1':
                df = df.loc[df['account_type'] == 'Federal Reserve Account'].drop(columns=['account_type']).reset_index(drop=True)
            return df
        except KeyError:
            return None

    def process_selected_fred_tables(self, selected_fred_tables):
        for table in selected_fred_tables:
            fred_df = self.process_fred_table(table)
            if fred_df is not None:
                self.all_dfs.append(fred_df)

    def process_selected_treasury_tables(self, selected_treasury_tables, treasury_columns):
        for table in selected_treasury_tables:
            treasury_df = self.process_treasury_table(table, treasury_columns)
            if treasury_df is not None:
                self.all_dfs.append(treasury_df)

    def merge_dataframes(self):
        table_df = self.all_dfs[0]
        for i in range(1, len(self.all_dfs)):
            table_df = pd.merge(table_df, self.all_dfs[i], on='date')

        return table_df

    def generate_null_report(self, table_df):
        table_df = table_df.replace('.', np.nan)
        col_null_values = table_df.isnull().sum()
        null_list = []
        for col_name, null_count in col_null_values.items():
            if null_count > 0:
                null_list.append(f"{col_name}: {null_count}")
        
        total_nulls_string = f"Total Null Values: {table_df.isnull().sum().sum()}"
        individual_nulls_string = ' | '.join(null_list)

        if len(null_list) > 0:
            individual_nulls_string = "Columns with Null Values: " + individual_nulls_string
        
        return total_nulls_string, individual_nulls_string