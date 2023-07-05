from dash_iconify import DashIconify
import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

fred_daily_select = dmc.MultiSelect(
    data=[
        {'label': 'S&P 500', 'value': 'SP500'},
        {'label': 'NASDAQ Composite', 'value': 'NASDAQCOM'},
    ],
    value=['SP500'],
    label="Federal Reserve Economic Data (FRED) Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={'text-align': 'center'},
    id='fred_daily_datasets'
)

treasury_daily_select = dmc.MultiSelect(
    data=[
        {'label': 'Treasury Balance', 'value': 'v1/accounting/dts/dts_table_1'},
        {'label': 'US Debt', 'value': 'v2/accounting/od/debt_to_penny'}
    ],
    value=['v1/accounting/dts/dts_table_1'],
    label="US Treasury Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={'text-align': 'center'},
    id='treasury_daily_datasets'
)

daily_start_year = dmc.NumberInput(
    label="Start Year",
    value=1980,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={'text-align': 'center'},
    id='daily_start_year_input'
)

daily_end_year = dmc.NumberInput(
    label="End Year",
    value=2023,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={'text-align': 'center'},
    id='daily_end_year_input'
)

daily_button = dmc.Button(
    "Request Selected Datasets",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    id='daily_button'
)

fred_monthly_select = dmc.MultiSelect(
    data=[
        # {'label': 'Case-Shiller Home Price Index', 'value': 'CSUSHPINSA'},
        {'label': 'CPI', 'value': 'CPIAUCSL'}
    ],
    value=['CPIAUCSL'],
    label="Federal Reserve Economic Data (FRED) Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={'text-align': 'center'},
    id='fred_monthly_datasets'
)

bea_monthly_select = dmc.MultiSelect(
    data=[
        {'label': 'Personal Income', 'value': 'T20600'},
        # {'label': "Percent Change in PCE", 'value': 'T20307'},
        # {'label': "Percent Change in Real PCE", 'value': 'T20301'},
        # {'label': "PCE Price Index", 'value':'T20304'}
    ],
    value=['T20600'],
    label="Bureau of Economic Analysis (BEA) Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={'text-align': 'center'},
    id='bea_monthly_datasets'
)

monthly_start_year = dmc.NumberInput(
    label="Start Year",
    value=1980,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={'text-align': 'center'},
    id='monthly_start_year_input'
)

monthly_end_year = dmc.NumberInput(
    label="End Year",
    value=2023,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={'text-align': 'center'},
    id='monthly_end_year_input'
)

monthly_button = dmc.Button(
    "Request Selected Datasets",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    id='monthly_button'
)

bea_quarterly_select = dmc.MultiSelect(
    data=[
        {'label': 'Percent Change in Real GDP', 'value': 'T10101'},
        {'label': 'Percent Change in GDP', 'value': 'T10107'},
        {'label': 'Total GDP in Dollars', 'value': 'T10105'},
        {'label': 'Personal Income', 'value': 'T20100'},
        {'label': "Percent Change in PCE", 'value': 'T20307'},
        {'label': "Percent Change in Real PCE", 'value': 'T20301'},
        {'label': "PCE Price Index", 'value':'T20304'}
    ],
    value=['T10101'],
    label="Bureau of Economic Analysis (BEA) Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={'text-align': 'center'},
    id='bea_quarterly_datasets'
)

fred_quarterly_select = dmc.MultiSelect(
    data=[
        {'label': 'CPI', 'value': 'CPIAUCSL'},
        {'label': 'Nonfarm Payrolls', 'value': 'PAYEMS'},
        {'label': 'Unemployment Rate', 'value': 'UNRATE'},
        {'label': "House Price Index", 'value':'USSTHPI'}
    ],
    value=['CPIAUCSL'],
    label="Federal Reserve Economic Data (FRED) Datasets",
    icon=DashIconify(icon='flat-color-icons:line-chart'),
    searchable=True,
    nothingFound="Dataset not found",
    style={'text-align': 'center'},
    id='fred_quarterly_datasets'
)

quarterly_start_year = dmc.NumberInput(
    label="Start Year",
    value=1950,
    min=1949,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={'text-align': 'center'},
    id='quarterly_start_year_input'
)

quarterly_end_year = dmc.NumberInput(
    label="End Year",
    value=2023,
    min=1940,
    max=2023,
    step=1,
    icon=DashIconify(icon='clarity:date-line'),
    style={'text-align': 'center'},
    id='quarterly_end_year_input'
)

quarterly_button = dmc.Button(
    "Request Selected Datasets",
    leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
    variant="gradient",
    id='quarterly_button'
)
