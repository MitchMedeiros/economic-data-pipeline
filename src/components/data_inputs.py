from dash_iconify import DashIconify
import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

start_year = dmc.NumberInput(
    label="Start Year",
    value=1980,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={"width": '150px', 'text-align': 'center'},
    id='start_year_input'
)

end_year = dmc.NumberInput(
    label="End Year",
    value=2023,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={"width": '150px', 'text-align': 'center'},
    id='end_year_input'
)

bea_select = dmc.MultiSelect(
    data=[
        {'label': 'Percent Change in Real GDP', 'value': 'T10101'},
        {'label': 'Percent Change in GDP', 'value': 'T10107'},
        {'label': 'Total GDP in Dollars', 'value': 'T10105'},
        # {'label': 'Personal Income', 'value': 'T20100'},
        {'label': 'Wages and Salaries by Industry', 'value': 'T20200B'},
        # {'label': 'Corporate Profits by Industry', 'value': 'T61600A'}
    ],
    value=['T10101'],
    label="BEA Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={"width": '350px', 'text-align': 'center'},
    id='bea_datasets'
)
# 'fxemoji:barchart'

fred_select = dmc.MultiSelect(
    data=[
        {'label': 'Quarterly CPI', 'value': 'CPIAUCSL'},
    ],
    value=['CPIAUCSL'],
    label="FRED Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={"width": '350px', 'text-align': 'center'},
    id='fred_datasets'
)

quarterly_button = dmc.Button(
    "Request Selected Datasets",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    style={'width': '300px', 'margin-left': 'auto', 'margin-right': 'auto'},
    id='quarterly_button'
)

treasury_select = dmc.MultiSelect(
    data=[
        {'label': 'Percent Change in Real GDP', 'value': 'T10101'},
        {'label': 'Percent Change in GDP', 'value': 'T10107'},
        {'label': 'Total GDP in Dollars', 'value': 'T10105'},
        # {'label': 'Personal Income', 'value': 'T20100'},
        {'label': 'Wages and Salaries by Industry', 'value': 'T20200B'},
        # {'label': 'Corporate Profits by Industry', 'value': 'T61600A'}
    ],
    value=['T10101'],
    label="US Treasury Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={"width": '350px', 'text-align': 'center'},
    id='treasury_datasets'
)

treasury_years = dmc.DateRangePicker(
    minDate=config.minimum_selectable_date,
    maxDate=config.maximum_selectable_date,
    value=[config.calendar_start, config.calendar_end],
    amountOfMonths=2,
    allowSingleDateInRange=True,
    clearable=False,
    icon=DashIconify(icon='clarity:date-line'),
    inputFormat="MMM DD, YYYY",
    style={"width": '350px'},
    id='treasury_dates'
)

daily_button = dmc.Button(
    "Request Selected Datasets",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    style={'width': '300px', 'margin-left': 'auto', 'margin-right': 'auto'},
    id='daily_button'
)
