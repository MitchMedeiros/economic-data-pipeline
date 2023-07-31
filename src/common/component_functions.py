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

def button(button_label, button_id, icon=DashIconify(icon="icon-park-twotone:data", color="white", width=24)):
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