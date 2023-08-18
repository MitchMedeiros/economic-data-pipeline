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

class DataCleaner:
    def __init__(self, time_interval, fred_api=None, fred_column_names=None, bea_api=None, bea_column_names=None,
                 bea_filter_metrics=None, treasury_api=None, treasury_column_names=None, treasury_columns=None):
        self.time_interval = time_interval
        self.all_dfs = []
        self.total_null_count = 0
        self.fred_api = fred_api
        self.fred_column_names = fred_column_names
        self.bea_api = bea_api
        self.bea_column_names = bea_column_names
        self.bea_filter_metrics = bea_filter_metrics
        self.treasury_api = treasury_api
        self.treasury_column_names = treasury_column_names
        self.treasury_columns = treasury_columns

    def process_fred_table(self, table):
        try:
            data = self.fred_api.data[table]['observations']
            df = pd.DataFrame(data, columns=['date', 'value']).rename(columns=self.fred_column_names[table])

            if self.time_interval == 'monthly':
                df['date'] = pd.to_datetime(df['date']).dt.to_period('M')

            if self.time_interval == 'quarterly':
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
        
    def process_bea_table(self, table):
        try:
            data = self.bea_api.data[table]['BEAAPI']['Results']['Data']
            df = pd.DataFrame(data, columns=['TimePeriod', 'DataValue', 'METRIC_NAME', 'LineDescription'])
            df = df.loc[df['LineDescription'] == self.bea_filter_metrics[table]].drop(columns=['LineDescription'])

            # Pivoting the table to have seperate columns for each distinct calculation method of the general economic metric.
            sliced_dfs = [
                df.loc[df['METRIC_NAME'] == metric]
                .drop(columns=['METRIC_NAME'])
                .reset_index(drop=True)
                .rename(columns={'DataValue': f'{self.bea_column_names[table]} - ' + metric})
                for metric in df['METRIC_NAME'].unique()
            ]
            pivoted_df = sliced_dfs[0]

            for i in range(1, len(sliced_dfs)):
                pivoted_df = pd.merge(pivoted_df, sliced_dfs[i], on='TimePeriod')
            pivoted_df.rename(columns={'TimePeriod': 'date'}, inplace=True)

            if self.time_interval == 'monthly':
                pivoted_df['date'] = pd.to_datetime(pivoted_df['date'], format='%YM%m').dt.to_period('M')
            return pivoted_df
        except KeyError:
            return dmc.Alert(
                title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                icon=DashIconify(icon='mingcute:alert-fill'),
                color='yellow',
                withCloseButton=True,
            ), False

    def process_treasury_table(self, table):
        try:
            data = self.treasury_api.data[table]['data']
            df = pd.DataFrame(data, columns=self.treasury_columns[table]).rename(columns=self.treasury_column_names[table])

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

    def process_all_fred_tables(self, selected_fred_tables):
        for table in selected_fred_tables:
            fred_df = self.process_fred_table(table)

            if fred_df is not None:
                self.all_dfs.append(fred_df)
    
    def process_all_bea_tables(self, selected_bea_tables):
        for table in selected_bea_tables:
            bea_df = self.process_bea_table(table)

            if bea_df is not None:
                self.all_dfs.append(bea_df)

    def process_all_treasury_tables(self, selected_treasury_tables):
        for table in selected_treasury_tables:
            treasury_df = self.process_treasury_table(table)

            if treasury_df is not None:
                self.all_dfs.append(treasury_df)

    def merge_dataframes(self):
        merged_df = self.all_dfs[0]
        for i in range(1, len(self.all_dfs)):
            merged_df = pd.merge(merged_df, self.all_dfs[i], on='date')
        if self.time_interval == 'monthly' or self.time_interval == 'quarterly':
            merged_df['date'] = merged_df['date'].astype(str)
        return merged_df

    def generate_null_report(self, df):
        df = df.replace('.', np.nan)
        column_null_values = df.isnull().sum()
        null_count_per_column = []
        for column_name, null_count in column_null_values.items():
            if null_count > 0:
                null_count_per_column.append(f"{column_name}: {null_count}")

        null_columns_string = ' | '.join(null_count_per_column)
        if len(null_count_per_column) > 0:
            null_columns_string = "Columns with Null Values: " + null_columns_string

        self.total_null_count = df.isnull().sum().sum()
            
        return null_columns_string
