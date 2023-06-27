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

def add_date_table(table, dataset_list):
    date_table_added = table not in dataset_list
    if date_table_added: dataset_list += [table]
    return date_table_added

def create_date_series(date_name, data):
    periods = [item[date_name] for item in data]
    unique_periods = list(set(periods))
    date_sr = pd.Series(unique_periods, name='date').sort_values().reset_index(drop=True)
    return date_sr

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

        add_bea_date_table = add_date_table('T10101', selected_bea_tables)

        BEA_BASE_URL = f"https://apps.bea.gov/api/data/"

        # The multiselect components' value: datasets, is a list of table names. This is converted to a dictionary of API endpoints.
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
            'T20100': "Personal income"
        }

        FRED_UNITS = "pch"
        FRED_FREQUENCY = "q"
        fred_start_year = f"{start_year}-01-01"
        fred_end_year = f"{end_year}-01-01"

        FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

        fred_endpoints = {
            f'{table}': (f"?series_id={table}"
                            f"&api_key={my_config.FRED_KEY}"
                            f"&file_type=json"
                            f"&observation_start={fred_start_year}"
                            f"&observation_end={fred_end_year}"
                            f"&units={FRED_UNITS}"
                            f"&frequency={FRED_FREQUENCY}"
                            f"&aggregation_method=sum")
            for table in selected_fred_tables
        }

        bea_api = RestAPI(BEA_BASE_URL, bea_endpoints)
        bea_api.fetch_data()

        date_sr = create_date_series('TimePeriod', bea_api.data['T10101']['BEAAPI']['Results']['Data'])

        if add_bea_date_table: selected_bea_tables.remove('T10101')

        def process_bea_table(bea_api, table, filter_metrics):
            try:
                data = bea_api.data[table]['BEAAPI']['Results']['Data']
                df = pd.DataFrame(data, columns=['DataValue', 'METRIC_NAME', 'LineDescription'])
            except KeyError:
                return dmc.Alert(
                    title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                    icon=DashIconify(icon='mingcute:alert-fill'),
                    color='yellow',
                    withCloseButton=True,
                ), False

            if table != 'T20307':
                df = df.loc[df['LineDescription'] == filter_metrics[table]].drop(columns=['LineDescription'])

            sliced_dfs = []
            unique_metrics = df['METRIC_NAME'].unique()
            for metric in unique_metrics:
                sliced_df = df.loc[df['METRIC_NAME'] == metric] \
                    .drop(columns=['METRIC_NAME']) \
                    .reset_index(drop=True) \
                    .rename(columns={'DataValue': f'{table} - ' + metric})
                sliced_dfs.append(sliced_df)

            pivoted_df = pd.concat(sliced_dfs, axis=1)
            return pivoted_df

        all_dfs = [date_sr]
        for table in selected_bea_tables:
            bea_df = process_bea_table(bea_api, table, filter_metrics)
            if bea_df is not None:
                all_dfs.append(bea_df)

        
        fred_api = RestAPI(FRED_BASE_URL, fred_endpoints)
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