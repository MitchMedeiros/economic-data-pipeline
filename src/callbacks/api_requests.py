import json

from dash import dash_table, html, Input, Output, State
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

def bea_api_callback(app):
    @app.callback(
        Output('bea_table', 'children'),
        Output('data_button', 'loading'),
        State('data_button', 'n_clicks'),
        Input('start_year_input', 'value'),
        State('end_year_input', 'value'),
        State('seasonal_checkbox', 'checked'),
        State('inflation_checkbox', 'checked'),
        State('bea_datasets', 'value'),
        prevent_initial_call=True
    )
    def get_bea_data(n_clicks, start_year, end_year, seasonal, inflation, datasets):
        bea_years = range(start_year, end_year + 1)

        bea_years = ','.join(str(year) for year in bea_years)
        bea_frequency = 'Q'
        bea_dataset = 'NIPA'
        bea_table = 'T10101'

        bea_base_url = f"https://apps.bea.gov/api/data/?&UserID={my_config.BEA_KEY}"
        bea_endpoints = {
            'gdp': f"&method=GetData \
                    &DataSetName={bea_dataset} \
                    &TableName={bea_table} \
                    &Frequency={bea_frequency} \
                    &Year={bea_years}"
        }

        bea_api = RestAPI(bea_base_url, bea_endpoints)
        bea_api.fetch_data()

        gdp_data = json.dumps(bea_api.data['gdp']['BEAAPI']['Results']['Data'])
        gdp_df = pd.read_json(gdp_data)
        gdp_df = (
            pd.DataFrame(gdp_df, columns=['TimePeriod', 'DataValue', 'METRIC_NAME', 'LineDescription'])
                .rename(columns={'TimePeriod': 'date', 'DataValue': 'gdp (%)', 'METRIC_NAME': 'metric'})
                .loc[gdp_df['LineDescription'] == "Gross domestic product"]
                .drop(columns=['LineDescription'])
        )

        return html.Div(
            dash_table.DataTable(
                data=gdp_df.to_dict('records'),
                columns=[{'name': str(i), 'id': str(i)} for i in gdp_df.columns],
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