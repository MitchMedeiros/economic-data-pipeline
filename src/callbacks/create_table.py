import psycopg2

import my_config

conn = psycopg2.connect(my_config.DB_CREDENTIALS)

query = '''
    SELECT
        table_name
    FROM
        information_schema.tables
    WHERE
        table_schema = 'public';
'''

def get_table_names(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)

    table_names = cursor.fetchall()
    cursor.close()
    connection.close()

    for table in table_names:
        print(table[0])
