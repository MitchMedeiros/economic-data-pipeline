from dash import Input, Output
import psycopg2

try:
    import my_config as config
except ImportError:
    import config

def table_dropdown_callback(app):
    @app.callback(
        Output('tables_dropdown', 'data'),
        Input('tables_button', 'n_clicks'),
        prevent_initial_call=True
    )
    def get_table_names(n_clicks):
        conn = psycopg2.connect(config.DB_CREDENTIALS)

        query = '''
            SELECT
                table_name
            FROM
                information_schema.tables
            WHERE
                table_schema = 'public';
        '''

        cursor = conn.cursor()
        cursor.execute(query)

        table_names = cursor.fetchall()
        cursor.close()
        conn.close()

        return [{'label': table[0], 'value': table[0]} for table in table_names]