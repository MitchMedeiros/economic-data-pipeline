from dash_iconify import DashIconify
import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

start_year = dmc.NumberInput(
    label="Start Year",
    # description="Start Date for the Data",
    value=1980,
    min=1940,
    max=2023,
    step=1,
    style={"width": '150px'},
    id='start_year_input'
)

end_year = dmc.NumberInput(
    label="End Year",
    # description="End Date for the Data",
    value=2023,
    min=1940,
    max=2023,
    step=1,
    style={"width": '150px'},
    id='end_year_input'
)

bea_select = dmc.MultiSelect(
    data=[
        {'label': 'Percent Change in Real GDP', 'value': 'T10101'},
        {'label': 'Personal Income', 'value': 'T20100'},
        {'label': 'Wages and Salaries by Industry', 'value': 'T20200A'},
        {'label': 'Corporate Profits by Industry', 'value': 'T61600A'}
    ],
    value='T10101',
    label="BEA Datasets",
    icon=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFound="Dataset not found",
    style={"width": 'auto', 'text-align': 'center'},
    id='bea_datasets'
)

seasonal_checkbox = dmc.Checkbox(
    color='green',
    label='Seasonally Adjusted',
    id='seasonal_checkbox'
)

inflation_checkbox = dmc.Checkbox(
    color='indigo',
    label='Inflation Adjusted',
    id='inflation_checkbox'
)

getdata_button = dmc.Button(
    "Request Data",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    # n_clicks=0,
    style={'width': '170px'},
    id='data_button'
)
