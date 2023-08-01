import src.common.component_functions as component_functions

# Daily Economic Data Components
fred_daily_select = component_functions.multiselect(
    [
        {'label': 'S&P 500', 'value': 'SP500'},
        {'label': 'NASDAQ Composite', 'value': 'NASDAQCOM'},
    ],
    ['SP500', 'NASDAQCOM'],
    "Federal Reserve Economic Data (FRED) Datasets",
    'fred_daily_datasets'
)

treasury_daily_select = component_functions.multiselect(
    [
        {'label': 'Treasury Balance', 'value': 'v1/accounting/dts/dts_table_1'},
        {'label': 'US Debt', 'value': 'v2/accounting/od/debt_to_penny'}
    ],
    ['v1/accounting/dts/dts_table_1', 'v2/accounting/od/debt_to_penny'],
    "US Treasury Datasets",
    'treasury_daily_datasets'
)

daily_start_year = component_functions.year("Start Year", 1980, 'daily_start_year_input')

daily_end_year = component_functions.year("End Year", 2023, 'daily_end_year_input')

daily_button = component_functions.button(
    "Request Selected Datasets",
    'daily_button',
    component_functions.icon('icon-park-twotone:data-display')
)

# Monthly Economic Data Components
fred_monthly_select = component_functions.multiselect(
    [
        {'label': 'Case-Shiller Home Price Index', 'value': 'CSUSHPINSA'},
        {'label': 'CPI', 'value': 'CPIAUCSL'}
    ],
    ['CPIAUCSL', 'CSUSHPINSA'],
    "Federal Reserve Economic Data (FRED) Datasets",
    'fred_monthly_datasets'
)

bea_monthly_select = component_functions.multiselect(
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

monthly_start_year = component_functions.year("Start Year", 1980, 'monthly_start_year_input')

monthly_end_year = component_functions.year("End Year", 2023, 'monthly_end_year_input')

monthly_button = component_functions.button(
    "Request Selected Datasets",
    'monthly_button',
    component_functions.icon('icon-park-twotone:data-display')
)

# Quarterly  Economic Data Components
bea_quarterly_select = component_functions.multiselect(
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

fred_quarterly_select = component_functions.multiselect(
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

quarterly_start_year = component_functions.year("Start Year", 1950, 'quarterly_start_year_input', min_year=1949)

quarterly_end_year = component_functions.year("End Year", 2023, 'quarterly_end_year_input')

quarterly_button = component_functions.button(
    "Request Selected Datasets",
    'quarterly_button',
    component_functions.icon('icon-park-twotone:data-display')
)
