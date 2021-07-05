import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    '''
    The function is used for loading the data into staging tables from S3 buckets.
    '''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''
    The function is used to insert the data into analytical tables from the staging tables. 
    '''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    # Reading configuration files
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Connection to a database in Redshift
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    # Load data from S3 buckets to Staging tables and from Staging to Analytical Tables
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()