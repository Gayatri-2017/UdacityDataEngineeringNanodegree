import redshift_connector
import configparser
from sql_queries import sql_queries_dict

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

def create_all_tables():
    conn = obtain_redshift_connector()

    cursor = conn.cursor()

    # sql_queries_config = dict(config.items('sql_queries'))
    

    create_tables_list = ["world_covid", "geocoding_mapping", "state_wise"]

    for table in create_tables_list:
        create_query = sql_queries_dict["create_{}_query".format(table)]
        cursor.execute(create_query)
    
    cursor.close()

    conn.commit()
    conn.close()

def copy_data_into_tables():

    copy_tables_list = ["world_covid"] 

    for table in copy_tables_list:
        copy_query = sql_queries_dict["copy_{}_query".format(table)]
        cursor.execute(copy_query)

    cursor.close()

    conn.commit()
    conn.close()



