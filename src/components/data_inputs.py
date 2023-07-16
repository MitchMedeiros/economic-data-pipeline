from dash_iconify import DashIconify
import dash_mantine_components as dmc

def request_data_multiselect(select_options, default_value, select_label, select_id):
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

def request_data_year(input_label, default_value, input_id, min_year=1940, max_year=2023):
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

def request_data_button(button_id):
    return dmc.Button(
        "Request Selected Datasets",
        leftIcon=DashIconify(icon="icon-park-twotone:data", color="white", width=24),
        variant="gradient",
        gradient={'from': 'grape', 'to': 'gray', 'deg': 45},
        className='general-button',
        id=button_id
    )

# Daily Economic Data Components
fred_daily_select = request_data_multiselect(
    [
        {'label': 'S&P 500', 'value': 'SP500'},
        {'label': 'NASDAQ Composite', 'value': 'NASDAQCOM'},
    ],
    ['SP500', 'NASDAQCOM'],
    "Federal Reserve Economic Data (FRED) Datasets",
    'fred_daily_datasets'
)
treasury_daily_select = request_data_multiselect(
    [
        {'label': 'Treasury Balance', 'value': 'v1/accounting/dts/dts_table_1'},
        {'label': 'US Debt', 'value': 'v2/accounting/od/debt_to_penny'}
    ],
    ['v1/accounting/dts/dts_table_1', 'v2/accounting/od/debt_to_penny'],
    "US Treasury Datasets",
    'treasury_daily_datasets'
)
daily_start_year = request_data_year("Start Year", 1980, 'daily_start_year_input')
daily_end_year = request_data_year("End Year", 2023, 'daily_end_year_input')
daily_button = request_data_button('daily_button')

# Monthly Economic Data Components
fred_monthly_select = request_data_multiselect(
    [
        {'label': 'Case-Shiller Home Price Index', 'value': 'CSUSHPINSA'},
        {'label': 'CPI', 'value': 'CPIAUCSL'}
    ],
    ['CPIAUCSL', 'CSUSHPINSA'],
    "Federal Reserve Economic Data (FRED) Datasets",
    'fred_monthly_datasets'
)
bea_monthly_select = request_data_multiselect(
    [
        {'label': 'Personal Income', 'value': 'T20600'},
        {'label': 'Percent Change in PCE', 'value': 'T20807'},
        {'label': 'Percent Change in Real PCE', 'value': 'T20801'},
        {'label': 'PCE Price Index', 'value': 'T20804'},
    ],
    ['T20600', 'T20804'],
    "Bureau of Economic Analysis (BEA) Datasets",
    'bea_monthly_datasets'
)
monthly_start_year = request_data_year("Start Year", 1980, 'monthly_start_year_input')
monthly_end_year = request_data_year("End Year", 2023, 'monthly_end_year_input')
monthly_button = request_data_button('monthly_button')

# Quarterly  Economic Data Components
bea_quarterly_select = request_data_multiselect(
    [
        {'label': 'Percent Change in GDP', 'value': 'T10107'},
        {'label': 'Percent Change in Real GDP', 'value': 'T10101'},
        {'label': 'Total GDP in Dollars', 'value': 'T10105'},
        {'label': 'Personal Income', 'value': 'T20100'},
        {'label': "Percent Change in PCE", 'value': 'T20307'},
        {'label': "Percent Change in Real PCE", 'value': 'T20301'},
        {'label': "PCE Price Index", 'value':'T20304'}
    ],
    ['T10107'],
    "Bureau of Economic Analysis (BEA) Datasets",
    'bea_quarterly_datasets'
)
fred_quarterly_select = request_data_multiselect(
    [
        {'label': 'CPI', 'value': 'CPIAUCSL'},
        {'label': 'Nonfarm Payrolls', 'value': 'PAYEMS'},
        {'label': 'Unemployment Rate', 'value': 'UNRATE'},
        {'label': "House Price Index", 'value':'USSTHPI'}
    ],
    ['CPIAUCSL', 'PAYEMS', 'UNRATE'],
    "Federal Reserve Economic Data (FRED) Datasets",
    'fred_quarterly_datasets'
)
quarterly_start_year = request_data_year("Start Year", 1950, 'quarterly_start_year_input', min_year=1949)
quarterly_end_year = request_data_year("End Year", 2023, 'quarterly_end_year_input')
quarterly_button = request_data_button('quarterly_button')
