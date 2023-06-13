from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import src.components.data_inputs as data_inputs
import src.components.strategy_inputs as strategy_inputs
import src.components.modals as modals

import io
import base64

from dash import Input, Output, State, dash_table
import pandas as pd

# The top bar of the app
page_header = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Stack(
                            [
                                html.Img(src='assets/favicon.ico', height="35px", style={'margin-left': '25px', 'margin-right': '25px'}),
                                dmc.Text(
                                    "Economic Data Requesting and Cleaning",
                                    variant='gradient',
                                    gradient={'from': '#52b1ff', 'to': '#739dff', 'deg': 45},
                                    style={'font-size': '25px'},
                                    id='page_title'
                                ),
                                dmc.Modal(
                                    children=modals.about_modal_children,
                                    centered=True,
                                    zIndex=100,
                                    size='xl',
                                    id='modal_4'
                                ),
                                dmc.Button(
                                    "About",
                                    leftIcon=DashIconify(icon='ep:info-filled', color='#739dff', height=20),
                                    variant='outline',
                                    color='indigo',
                                    size='lg',
                                    compact=True,
                                    radius='xl',
                                    style={'margin-left': '50px'},
                                    id='icon_4'
                                )
                            ],
                            direction='horizontal',
                            gap=2,
                            style={'margin-left': '25px'}
                        )
                    ]
                )
            ],
            justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            [
                                dmc.Tooltip(
                                    [
                                        dmc.ThemeIcon(
                                            DashIconify(icon='line-md:github-loop', width=30),
                                            size='xl',
                                            radius='xl',
                                            variant='outline',
                                            color='indigo'
                                        )
                                    ],
                                    label="GitHub Repository",
                                    position="bottom"
                                )
                            ],
                            href="https://github.com/MitchMedeiros/economic-data",
                            target="_blank"
                        )
                    ],
                    style={'margin-right': '40px', 'margin-left': '20px'}
                ),
                dbc.Col(
                    [
                        dmc.Switch(
                            offLabel=DashIconify(icon='line-md:moon-rising-twotone-loop', width=20),
                            onLabel=DashIconify(icon='line-md:sun-rising-loop', width=20),
                            size='xl',
                            color='indigo',
                            style={'margin-right': '15px'},
                            id='theme_switch'
                        )
                    ]
                )
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center"
        )
    ],
    color='#2b2b2b',
    style={'margin-bottom': '7px', 'padding': '10px', 'background-color': '#2b2b2b'},
    id='page_header'
)

def accordion_header(displayed_text):
    return dmc.Badge(
        displayed_text,
        variant='gradient',
        gradient={'from': 'blue', 'to': 'violet'},
        opacity=0.85,
        size='lg',
        radius='md',
        style={'width': '100%'}
    )

tab_style = {'padding': '4px', 'padding-top': '9px'}
selected_tab_style = {'padding': '4px', 'padding-top': '7px'}

# The main section of the app where data is displayed. Contains three tabs.
data_area = dmc.LoadingOverlay(
    [
        dmc.AccordionMultiple(
            [
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(accordion_header("Request Economic Data")),
                        dmc.AccordionPanel(
                            [
                                data_inputs.date_calendar,
                                strategy_inputs.run_backtest_button
                            ]
                        )
                    ],
                    value='request'
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(accordion_header("Check Cleanliness of Data")),
                        dmc.AccordionPanel()
                    ],
                    value='analyze'
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(accordion_header("Clean Data if Needed")),
                        dmc.AccordionPanel()
                    ],
                    value='clean'
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(accordion_header("Visualize and Save Data")),
                        dmc.AccordionPanel()
                    ],
                    value='compare'
                )
            ],
            value=['request', 'analyze', 'clean', 'compare'],
            chevronPosition='left',
            styles={'chevron': {"&[data-rotate]": {'transform': 'rotate(-90deg)'}}}
        )
    ],
    loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
    radius='sm'
)

def make_datatable(app):
    @app.callback(
        Output('upload_output', 'children'),
        Input('upload_input', 'contents'),
        State('upload_input', 'filename'),
        prevent_initial_call=True
    )
    def update_output(content, filename):
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return dmc.Text('There was an error processing this file.')

        return html.Div(
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': str(i), 'id': str(i)} for i in df.columns],
                fill_width=True,
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
        )

# The app layout containing all displayed components. Provided to app.layout in main.py
def create_layout():
    return dmc.MantineProvider(
        dmc.NotificationsProvider(
            [
                dbc.Container(
                    [
                        page_header,
                        dbc.Row(dbc.Col(data_area, style={'overflow': 'hidden'})),
                        html.Div(id='dummy_output'),
                        html.Div(id='notification_trigger'),
                        html.Div(id='notification_output'),
                        dmc.LoadingOverlay(
                            [
                                dcc.Upload(
                                    html.Div(
                                        [
                                            'Drag and Drop or ',
                                            html.A('Select a File', style={'fontWeight': 'bold'}),
                                            ' (20MB limit)'
                                        ]
                                    ),
                                    style={
                                        'height': '80px',
                                        'lineHeight': '75px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },
                                    style_reject={'borderColor': 'rgb(255, 20, 20)', 'backgroundColor': 'rgb(255, 20, 20)'},
                                    max_size=20000000,
                                    min_size=50,
                                    id='upload_input'
                                ),
                                html.Div(id='upload_output')
                            ],
                            loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
                            radius='sm',
                            style={'width': '95%', 'margin-left': 'auto', 'margin-right': 'auto'}
                        )
                    ],
                    fluid=True,
                    className='dbc'
                )
            ],
            position='bottom-center',
            containerWidth='45%'
        ),
        theme={'colorScheme': 'dark'},
        id='mantine_container'
    )
