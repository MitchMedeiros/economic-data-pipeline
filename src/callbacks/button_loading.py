from dash import clientside_callback, Input, Output

# Changes the run backtest button state to loading when clicked
clientside_callback(
    '''
    function(n_clicks) {
        return true
    }
    ''',
    Output("daily_button", "loading", allow_duplicate=True),
    Input("daily_button", "n_clicks"),
    prevent_initial_call=True
)

clientside_callback(
    '''
    function(n_clicks) {
        return true
    }
    ''',
    Output("monthly_button", "loading", allow_duplicate=True),
    Input("monthly_button", "n_clicks"),
    prevent_initial_call=True
)

clientside_callback(
    '''
    function(n_clicks) {
        return true
    }
    ''',
    Output("quarterly_button", "loading", allow_duplicate=True),
    Input("quarterly_button", "n_clicks"),
    prevent_initial_call=True
)
