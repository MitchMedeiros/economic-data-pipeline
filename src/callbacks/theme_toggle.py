from dash import clientside_callback, Input, Output

# Changes the app theme based on the theme switch position. Initially suppress it to prevent flickering.
clientside_callback(
    """
    function change_theme(checked) {
        const theme1 = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
        const theme2 = "https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/darkly/bootstrap.min.css"
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]')
        var themeLink = checked ? theme1 : theme2;

        stylesheet.href = themeLink
    }
    """,
    Output('dummy_output', 'children'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)

# Changes the color scheme of mantine components and various background and text colors.
clientside_callback(
    '''
    function change_layout_colors(checked) {
        var components_color = {colorScheme: checked ? 'light' : 'dark'};
        var header_color = checked ? '#d5d5d5' : '#2b2b2b';
        var page_title = checked ? {'from': 'rgb(252, 62, 211)', 'to': 'rgb(255, 31, 199)', 'deg': 45} : {'from': 'rgb(255, 117, 165)', 'to': 'rgb(245, 134, 255)', 'deg': 45};

        return [components_color, header_color, page_title];
    }
    ''',
    Output('mantine_container', 'theme'),
    Output('page_header', 'color'),
    Output('page_title', 'gradient'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)
