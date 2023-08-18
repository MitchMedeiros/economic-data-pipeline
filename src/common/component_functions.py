from dash import dash_table, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

def multiselect(select_options, default_value, select_label, select_id):
    return dmc.MultiSelect(
        data=select_options,
        value=default_value,
        label=select_label,
        icon=DashIconify(icon='flat-color-icons:line-chart'),
        searchable=True,
        nothingFound="Dataset not found",
        className='general-multiselect',
        id=select_id
    )

def year(input_label, default_value, input_id, min_year=1940, max_year=2023):
    return dmc.NumberInput(
        label=input_label,
        value=default_value,
        min=min_year,
        max=max_year,
        step=1,
        icon=DashIconify(icon='clarity:date-line'),
        className='general-number-input',
        id=input_id
    )

def button(button_label, button_id, icon=None):
    return dmc.Button(
        button_label,
        leftIcon=icon,
        variant="gradient",
        gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
        className='general-button',
        id=button_id
    )

def checkbox(checkbox_label, checkbox_id):
    return dmc.Checkbox(
        label=checkbox_label,
        checked=False,
        className='general-checkbox',
        id=checkbox_id
    )

def select(select_options, default_value, select_label, select_id):
    return dmc.Select(
        data=select_options,
        value=default_value,
        label=select_label,
        searchable=True,
        nothingFound="Option not found",
        className='general-select',
        id=select_id
    )

def accordion_header(displayed_text):
    return dmc.Badge(
        displayed_text,
        variant='gradient',
        gradient={'from': 'rgb(192, 135, 192)', 'to': 'rgb(106, 79, 101)'},
        opacity=0.99,
        size='lg',
        radius='md',
        style={'width': '100%'}
    )

def request_data_header(text):
    return dmc.Text(
        text,
        size=18,
        weight=600,
        align='center'
    )

def request_data_column(header_text, year_inputs, button, *multiselects):
    return dbc.Col(
        dbc.Stack(
            [
                dmc.Text(header_text, size=18, weight=600, align='center'),
                *multiselects,
                dbc.Stack(
                    year_inputs,
                    direction='horizontal',
                    gap=3
                ),
                button
            ],
            gap=3
        )
    )

def icon(icon_name):
    return DashIconify(
        icon=icon_name,
        color="white",
        width=24
    )

def datatable(header, total_null_values, null_columns_string, df):
    return [
        dmc.Text(header, weight=550, size='lg', style={'margin-top': '10px', 'margin-bottom': '10px'}),
        dmc.Text(total_null_values, weight=410, size='sm', className='general-text'),
        dmc.Text(null_columns_string, weight=410, size='sm', className='general-text'),
        html.Div(
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': str(i), 'id': str(i)} for i in df.columns],
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
                id='monthly_dash_table'
            )
        )
    ]
