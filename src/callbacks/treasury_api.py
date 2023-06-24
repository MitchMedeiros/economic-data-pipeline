from dash import dash_table, html, Input, Output, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import pandas as pd
import requests

from . bea_fred_api import RestAPI
import my_config

def bea_fred_callback(app):
    @app.callback(
        Output('bea_table', 'children'),
        Output('daily_button', 'loading'),
        Input('daily_button', 'n_clicks'),
        State('treasury_dates', 'value'),
        State('treasury_datasets', 'value'),   
        prevent_initial_call=True
    )
    def get_bea_data(n_clicks, dates, selected_treasury_tables):
        all_years_string = range(start_year, end_year + 1)
        all_years_string = ','.join(str(year) for year in all_years_string)

        treasury_base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
        treasury_endpoints = {
            f'{table}': f"{table}?&filter=record_fiscal_year:in:({all_years_string})" for table in selected_treasury_tables
        }

        treasury_api = RestAPI(treasury_base_url, treasury_endpoints)
        treasury_api.fetch_data()

        for table in selected_treasury_tables:
            if table == 'v1/accounting/dts/dts_table_1':
                try:
                    treasury_api.data[table] = (
                        pd.DataFrame(treasury_api.data[table]['data'], columns=['record_date', 'close_today_bal', 'account_type']) \
                        .rename(columns={'close_today_bal': 'closing_daily_balance'}))
                except KeyError:
                    return dmc.Alert(
                        title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                        icon=DashIconify(icon='mingcute:alert-fill'),
                        color='yellow',
                        withCloseButton=True,
                    ), False

                treasury_api.data[table] = (
                    treasury_api.data[table].loc[treasury_api.data[table]['account_type'] == 'Federal Reserve Account']
                    .drop(columns=['account_type'])).reset_index(drop=True)
            elif table == 'v2/accounting/od/debt_to_penny':
                try:
                    treasury_api.data[table] = (
                        pd.DataFrame(treasury_api.data[table]['data'], columns=['record_date', 'transaction_type', 'transaction_today_amt']) \
                        .rename(columns={'transaction_today_amt': 'amount ($M)'}))
                    treasury_api.data[table] = treasury_api.data[table].astype({"transaction_type": str, "amount ($M)": float})
                except KeyError:
                    return dmc.Alert(
                        title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                        icon=DashIconify(icon='mingcute:alert-fill'),
                        color='yellow',
                        withCloseButton=True,
                    ), False

                treasury_api.data[table] = (
                    treasury_api.data[table]
                    .groupby(['record_date', 'transaction_type'])['amount ($M)']
                    .sum()
                    .reset_index()
                    # .drop(columns=['record_date'])
                )

                sliced_dfs = []
                unique_metrics = treasury_api.data[table]['transaction_type'].unique()
                for metric in unique_metrics:
                    sliced_df = (
                        treasury_api.data[table].loc[treasury_api.data[table]['transaction_type'] == metric]
                        .drop(columns=['transaction_type'])
                        .reset_index(drop=True)
                        .rename(columns={'amount ($M)': f'{metric} ' + 'amount ($M)'})
                    )
                    sliced_dfs.append(sliced_df)
                merged_df = pd.concat(sliced_dfs, axis=1)

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