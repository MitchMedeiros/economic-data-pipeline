from dash_iconify import DashIconify
import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

date_calendar = dmc.DateRangePicker(
    minDate=config.minimum_selectable_date,
    maxDate=config.maximum_selectable_date,
    value=[config.calendar_start, config.calendar_end],
    amountOfMonths=2,
    allowSingleDateInRange=True,
    clearable=False,
    icon=DashIconify(icon='clarity:date-line'),
    inputFormat="MMM DD, YYYY",
    style={"width": '238px'},
    id='date_range'
)
