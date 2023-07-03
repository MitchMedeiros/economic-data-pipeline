from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import src.components.data_inputs as data_inputs
import src.components.modals as modals

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
                                    "Economic and Financial Data",
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
                                    id='modal_1'
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
                                    id='icon_1'
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

# The main section of the app where data is displayed. Contains three tabs.
data_area = dmc.LoadingOverlay(
    [
        dmc.AccordionMultiple(
            [
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(accordion_header("Request Data")),
                        dmc.AccordionPanel(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Stack(
                                            [   
                                                dmc.Text("Daily Economic Data", color='blue', size=18, weight=600, align='center'),
                                                data_inputs.fred_daily_select,
                                                data_inputs.treasury_daily_select,
                                                dbc.Stack(
                                                    [
                                                        data_inputs.daily_start_year,
                                                        data_inputs.daily_end_year,
                                                    ],
                                                    direction='horizontal',
                                                    gap=3
                                                ),
                                                data_inputs.daily_button
                                            ],
                                            gap=3
                                        )),
                                        # dbc.Col(dmc.Divider(color='indigo', size='md', orientation="vertical", style={"height": '300px'})),
                                        dbc.Col(dbc.Stack(
                                            [   
                                                dmc.Text("Monthly Economic Data", color='blue', size=18, weight=600, align='center'),
                                                data_inputs.fred_monthly_select,                                                
                                                dbc.Stack(
                                                    [
                                                        data_inputs.monthly_start_year,
                                                        data_inputs.monthly_end_year,
                                                    ],
                                                    direction='horizontal',
                                                    gap=3
                                                ),
                                                data_inputs.monthly_button
                                            ],
                                            gap=3
                                        )),
                                        # dbc.Col(dmc.Divider(color='indigo', size='md', orientation="vertical", style={"height": '300px'})),
                                        dbc.Col(dbc.Stack(
                                            [
                                                dmc.Text("Quarterly Economic Data", color='blue', size=18, weight=600, align='center'),
                                                data_inputs.fred_quarterly_select,
                                                data_inputs.bea_quarterly_select,
                                                dbc.Stack(
                                                    [
                                                        data_inputs.quarterly_start_year,
                                                        data_inputs.quarterly_end_year,
                                                    ],
                                                    direction='horizontal',
                                                    gap=3
                                                ),
                                                data_inputs.quarterly_button
                                            ],
                                            gap=3
                                        ))
                                    ]
                                )
                            ]
                        )
                    ],
                    value='request'
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(accordion_header("Check Cleanliness of Data")),
                        dmc.AccordionPanel(
                            [
                                html.Div(id='daily_table', style={'max-height': '300px', 'overflow-y': 'auto'}),        
                                html.Div(id='monthly_table', style={'max-height': '300px', 'overflow-y': 'auto'}),                        
                                html.Div(id='quarterly_table', style={'max-height': '300px', 'overflow-y': 'auto'}),
                            ]
                        )
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

# The app layout containing all displayed components. Provided to app.layout in main.py
def create_layout():
    return dmc.MantineProvider(
        dmc.NotificationsProvider(
            [
                dmc.Container(
                    [
                        page_header,
                        data_area,
                        html.Div(id='dummy_output'),
                        html.Div(id='notification_trigger'),
                        html.Div(id='notification_output'),
                    ],
                    fluid=True,
                    className='dbc'
                )
            ],
            position='bottom-center',
            containerWidth='38%'
        ),
        theme={'colorScheme': 'dark'},
        id='mantine_container'
    )
