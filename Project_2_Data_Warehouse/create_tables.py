import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    '''
    The method drop tables if the tables are already existing in Redshift
    '''
    for query in drop_table_queries:
        print("query = \n", query)
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    '''
    The method create new tables in Redshift
    '''
    for query in create_table_queries:
        print("query = \n", query)
        cur.execute(query)
        conn.commit()


def main():
    # Reading configuration files
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    # Connection to a database in Redshift
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    #  Drop existing tables, if any and create new tables
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()