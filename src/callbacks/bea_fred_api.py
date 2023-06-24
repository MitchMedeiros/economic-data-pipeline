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
        for key, endpoint in self.endpoints.items():
            url = self.base_url + endpoint
            response = requests.get(url)
            if response.status_code == 200: self.data[key] = response.json()

'''
BEA Endpoint Descriptions:
"gdp" - Percent Change From Preceding Period in Real Gross Domestic Product (A) (Q).
'''

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
    def get_bea_data(n_clicks, start_year, end_year, selected_bea_tables, selected_fred_tables):
        all_years_string = range(start_year, end_year + 1)
        all_years_string = ','.join(str(year) for year in all_years_string)

        if 'T10101' not in selected_bea_tables: 
            selected_bea_tables += ['T10101']
            T10101_added = True
        else: 
            T10101_added = False

        bea_base_url = f"https://apps.bea.gov/api/data/"

        # The multiselect components' value: datasets, is a list of table names.
        # We can use dictionary comprehension to create the endpoints from this, with the table names are used as the keys.
        bea_endpoints = {
            f'{table}': (f"?&UserID={my_config.BEA_KEY}"
                        f"&method=GetData"
                        f"&DataSetName=NIPA"
                        f"&Frequency=Q"
                        f"&TableName={table}"
                        f"&Year={all_years_string}")
            for table in selected_bea_tables
        }

        # In general, each table contains multiple economic metrics, for example, gross domestic product and gross national product.
        # We can use a dictionary to filter on the metric we're interested in per table rather than doing several if statements.
        filter_metrics = {
            "T10101": "Gross domestic product",
            'T10105': "Gross domestic product",
            'T10107': "Gross domestic product",
            'T20100': "Personal income",
            'T20200B': "Wages and salaries",
            'T61600A': "test"
        }

        bea_api = RestAPI(bea_base_url, bea_endpoints)
        bea_api.fetch_data()

        # Creating a date series to index the user selected DataFrames.
        periods = [item['TimePeriod'] for item in bea_api.data['T10101']['BEAAPI']['Results']['Data']]
        unique_periods = list(set(periods))
        date_sr = pd.Series(unique_periods, name='date').sort_values().reset_index(drop=True)

        if T10101_added: selected_bea_tables.remove('T10101')

        # Replacing the JSON data within the bea_api.data dictionary with formatted DataFrames.
        all_dfs = [date_sr]
        for table in selected_bea_tables:
            try:
                bea_api.data[table] = (
                    pd.DataFrame(bea_api.data[table]['BEAAPI']['Results']['Data'], columns=['DataValue', 'METRIC_NAME', 'LineDescription']) \
                    .rename(columns={'DataValue': table + '_value', 'METRIC_NAME': table + '_metric'}))
            except KeyError:
                return dmc.Alert(
                    title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                    icon=DashIconify(icon='mingcute:alert-fill'),
                    color='yellow',
                    withCloseButton=True,
                ), False
            bea_api.data[table] = (
                bea_api.data[table].loc[bea_api.data[table]['LineDescription'] == filter_metrics[table]]
                .drop(columns=['LineDescription']))

            # The tables contain multiple values for a given economic measure using differnt methodologies. These are vertically stacked.
            # To avoid needing to filter on the method column, the table is pivotted in a way that doesn't produce NaN values:
            sliced_dfs = []
            unique_metrics = bea_api.data[table][table + '_metric'].unique()
            for metric in unique_metrics:
                sliced_df = (
                    bea_api.data[table].loc[bea_api.data[table][table + '_metric'] == metric]
                    .drop(columns=[table + '_metric'])
                    .reset_index(drop=True)
                    .rename(columns={f'{table}_value': f'{table} - ' + metric})
                )
                sliced_dfs.append(sliced_df)
            merged_df = pd.concat(sliced_dfs, axis=1)
            all_dfs.append(merged_df)

        fred_units = "pch"
        fred_frequency = "q"
        fred_start_year = f"{start_year}-01-01"
        fred_end_year = f"{end_year}-01-01"

        fred_base_url = "https://api.stlouisfed.org/fred/series/observations"

        fred_endpoints = {
            f'{table}': (f"?series_id={table}"
                            f"&api_key={my_config.FRED_KEY}"
                            f"&file_type=json"
                            f"&observation_start={fred_start_year}"
                            f"&observation_end={fred_end_year}"
                            f"&units={fred_units}"
                            f"&frequency={fred_frequency}"
                            f"&aggregation_method=sum")
            for table in selected_fred_tables
        }
        
        fred_api = RestAPI(fred_base_url, fred_endpoints)
        fred_api.fetch_data()

        for table in selected_fred_tables:
            try:
                fred_df = (
                    pd.DataFrame(fred_api.data[table]['observations'], columns=['value']) \
                    .rename(columns={'value': table + '_value'}))
            except KeyError:
                return dmc.Alert(
                    title="There was a problem requesting the selected data from FRED.",
                    icon=DashIconify(icon='mingcute:alert-fill'),
                    color='yellow',
                    withCloseButton=True,
                ), False
            all_dfs.append(fred_df)

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