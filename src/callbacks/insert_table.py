from dash import html, Input, Output, State
import dash_mantine_components as dmc
import psycopg2
from psycopg2 import Error, extras

try:
    import my_config as config
except ImportError:
    import config

def insert_table_callback(app):
    @app.callback(
        Output('insert_error_div', 'children'),
        Input('save_button', 'n_clicks'),
        State('clean_data', 'data'),
        prevent_initial_call=True
    )
    def insert_table(n_clicks):
        try:
            conn = psycopg2.connect(config.DB_CREDENTIALS)

            create_table_query = '''
                CREATE TABLE
                    your_table_name (
                    column1 datatype1,
                    column2 datatype2
                    );
            '''

            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

            data = df.values.tolist()  # Convert dataframe to list of tuples

            insert_query = "INSERT INTO your_table_name (column1, column2, ...) VALUES %s"
            psycopg2.extras.execute_values(cursor, insert_query, data)
            conn.commit()

            cursor.close()
            conn.close()
        except Exception:
            return dmc.Alert()
