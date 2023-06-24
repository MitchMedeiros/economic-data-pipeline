from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from flask_caching import Cache

import src.callbacks.bea_fred_api as bea_fred_api
import src.callbacks.button_loading
import src.callbacks.children as children
import src.callbacks.modals as modals
import src.callbacks.theme_toggle
import src.components.layout as layout

try:
    import my_config as config
except ImportError:
    import config

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiate the dash app.
app = Dash(
    __name__,
    external_stylesheets=[DARKLY, dbc_css],
    serve_locally=config.LOCALLY_STYLE,
    suppress_callback_exceptions=config.CALLBACK_SUPPRESS,
    title='Economic Data App',
    update_title='Loading...'
)

# Name the webserver object. This is passed to the wsgi and flask-cache.
server = app.server

# Instantiate the flask cache
if config.CACHE_TYPE == 'redis':
    cache = Cache(config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_HOST': config.REDIS_HOST,
        'CACHE_REDIS_PORT': config.REDIS_PORT
    })
elif config.CACHE_TYPE == 'files':
    cache = Cache(config={
        'CACHE_TYPE': 'FileSystemCache',
        'CACHE_DIR': config.CACHE_DIRECTORY,
        'CACHE_THRESHOLD': config.CACHE_SIZE,
        'CACHE_OPTIONS': config.PERMISSIONS
    })
cache.init_app(app.server)

# Provide the layout, containing all the dash components to be displayed.
app.layout = layout.create_layout()

# Instantiate the imported callbacks. The clientside callbacks are instantiated via module import.
modals.modal_callbacks(app)
children.notification_callback(app)
bea_fred_api.bea_fred_callback(app)

# Deploys the app locally if run_locally is True.
if __name__ == '__main__' and config.RUN_LOCALLY:
    app.run(debug=config.DEBUG_BOOL, port=config.PORT_NUMBER)
