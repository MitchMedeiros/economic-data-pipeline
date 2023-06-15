from dash import clientside_callback, Input, Output

# Changes the run backtest button state to loading when clicked
clientside_callback(
    '''
    function(n_clicks) {
        return true
    }
    ''',
    Output("data_button", "loading", allow_duplicate=True),
    Input("data_button", "n_clicks"),
    prevent_initial_call=True
)
