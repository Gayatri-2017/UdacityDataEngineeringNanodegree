import redshift_connector
import configparser

def get_redshift_config():
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    redshift_connection_config = dict(config.items('redshift_connection'))

    return redshift_connection_config

def obtain_redshift_connector():
# Connects to Redshift cluster using AWS credentials
    redshift_connection_config = get_redshift_config()
    conn = redshift_connector.connect(
        host=redshift_connection_config["host"],
        database=redshift_connection_config["database"],
        user=redshift_connection_config["user"],
        password=redshift_connection_config["password"]
     )
    return conn

def execute_select_dataframe(query=None):
    if query:
        conn = obtain_redshift_connector()

        cursor = conn.cursor()
        df = cursor.execute(query).fetch_dataframe()
        cursor.close()

        conn.commit()
        conn.close()

        return df

def execute_insert(query=None, values=None):
    if query:
        conn = obtain_redshift_connector()

        cursor = conn.cursor()
        cursor.execute(query, values)
        cursor.close()

        conn.commit()
        conn.close()
