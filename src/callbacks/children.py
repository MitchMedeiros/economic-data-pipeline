from dash import Input, Output
from dash_iconify import DashIconify
import dash_mantine_components as dmc

# A dummy input and output div is used to trigger the notification popup on page load only and keep it
# seperated from other callbacks.
def notification_callback(app):
    @app.callback(
        Output('notification_output', 'children'),
        Input('notification_trigger', 'children')
    )
    def show(children):
        return dmc.Notification(
            action='show',
            title=dmc.Text(
                "Click the About button in the top bar of the page to learn more about what this app does.",
                size='17px'
            ),
            message=None,
            icon=DashIconify(icon='ant-design:notification-filled', color='orange'),
            color='indigo',
            autoClose=20000,
            id='initial_message'
        )
