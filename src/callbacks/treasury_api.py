from dash import dash_table, html, Input, Output, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import pandas as pd

from . bea_fred_api import RestAPI

def treasury_callback(app):
    @app.callback(
        Output('treasury_table', 'children'),
        Output('daily_button', 'loading'),
        Input('daily_button', 'n_clicks'),
        State('treasury_dates', 'value'),
        State('treasury_datasets', 'value'),   
        prevent_initial_call=True
    )
    def get_bea_data(n_clicks, dates, selected_treasury_tables):
        start_year = 2016
        end_year = 2022

        all_years_string = range(start_year, end_year + 1)
        all_years_string = ','.join(str(year) for year in all_years_string)

        if 'v1/accounting/dts/dts_table_1' not in selected_treasury_tables: 
            selected_treasury_tables += ['v1/accounting/dts/dts_table_1']
            dts_table_1_added = True
        else: 
            dts_table_1_added = False

        treasury_base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
        treasury_endpoints = {
            f'{table}': f"{table}?&filter=record_fiscal_year:in:({all_years_string})" for table in selected_treasury_tables
        }

        treasury_api = RestAPI(treasury_base_url, treasury_endpoints)
        treasury_api.fetch_data()

        # Creating a date series to index the user selected DataFrames.
        periods = [item['record_date'] for item in treasury_api.data['v1/accounting/dts/dts_table_1']['data']]
        unique_periods = list(set(periods))
        date_sr = pd.Series(unique_periods, name='date').sort_values().reset_index(drop=True)

        if dts_table_1_added: selected_treasury_tables.remove('v1/accounting/dts/dts_table_1')

        table_columns = {
            'v1/accounting/dts/dts_table_1': ['close_today_bal', 'account_type'],
            'v2/accounting/od/debt_to_penny': ['tot_pub_debt_out_amt']
        }

        table_column_names = {
            'v1/accounting/dts/dts_table_1': {'close_today_bal': 'closing_daily_balance'},
            'v2/accounting/od/debt_to_penny': {'tot_pub_debt_out_amt': 'Total_Outstanding_Debt'}
        }

        # Replacing the JSON data within the bea_api.data dictionary with formatted DataFrames.
        all_dfs = [date_sr]
        for table in selected_treasury_tables:
            try:
                treasury_api.data[table] = (
                    pd.DataFrame(treasury_api.data[table]['data'], columns=table_columns[table]) \
                    .rename(columns=table_column_names[table]))
            except KeyError:
                return dmc.Alert(
                    title="Invalid Years: No data is available within the selected years for one of the requested datasets.",
                    icon=DashIconify(icon='mingcute:alert-fill'),
                    color='yellow',
                    withCloseButton=True,
                ), False

            if table == 'v1/accounting/dts/dts_table_1':
                treasury_api.data[table] = (
                    treasury_api.data[table].loc[treasury_api.data[table]['account_type'] == 'Federal Reserve Account']
                    .drop(columns=['account_type'])).reset_index(drop=True)

            all_dfs.append(treasury_api.data[table])
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
