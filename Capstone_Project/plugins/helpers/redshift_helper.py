import redshift_connector
import configparser

from plugins.helpers.sql_queries import SqlQueries

class RedshiftHelper:
    
    def get_redshift_config(self):
        config = configparser.RawConfigParser()
        config.read('config.cfg')

        return dict(config.items('redshift_connection'))

    def get_aws_config(self):
        config = configparser.RawConfigParser()
        config.read('config.cfg')

        return dict(config.items('aws_connection'))

    def obtain_redshift_connector(self):
    # Connects to Redshift cluster using AWS credentials
        redshift_connection_config = self.get_redshift_config()
        conn = redshift_connector.connect(
            host=redshift_connection_config["host"],
            database=redshift_connection_config["database"],
            user=redshift_connection_config["user"],
            password=redshift_connection_config["password"]
         )
        return conn

    def execute_select_dataframe(self, query=None):
        if query:
            conn = self.obtain_redshift_connector()

            cursor = conn.cursor()
            df = cursor.execute(query).fetch_dataframe()
            cursor.close()

            conn.commit()
            conn.close()

            return df

    def execute_insert(self, query=None, values=None):
        if query:
            conn = self.obtain_redshift_connector()

            cursor = conn.cursor()
            cursor.execute(query, values)
            cursor.close()

            conn.commit()
            conn.close()

    def execute_insert_select(self, query=None):
        if query:
            conn = self.obtain_redshift_connector()

            # print("query = ", query)
            cursor = conn.cursor()
            cursor.execute(query)
            cursor.close()

            conn.commit()
            conn.close()            

    def create_all_tables(self):
        conn = self.obtain_redshift_connector()
        cursor = conn.cursor()

        create_tables_list = ["world_covid", "geocoding_mapping", "state_wise_trend"]

        for table in create_tables_list:
            create_query = SqlQueries.sql_queries_dict["create_{}_query".format(table)]
            cursor.execute(create_query)
        
        cursor.close()

        conn.commit()
        conn.close()

    def copy_data_into_tables(self):

        aws_connection_config = self.get_aws_config()
        copy_tables_list = ["world_covid"] 

        conn = self.obtain_redshift_connector()
        cursor = conn.cursor()

        for table in copy_tables_list:
            copy_query = SqlQueries.sql_queries_dict["copy_{}_query".format(table)].format(aws_access_key_id=aws_connection_config["aws_access_key_id"],
                                                                                aws_secret_access_key=aws_connection_config["aws_secret_access_key"])
            cursor.execute(copy_query)

        cursor.close()

        conn.commit()
        conn.close()

    def check_no_data_exists(self):

        conn = self.obtain_redshift_connector()
        cursor = conn.cursor()

        check_tables_list = ["state_wise_trend"]

        for table in check_tables_list:
            check_query = SqlQueries.sql_queries_dict["check_no_data_exists"].format(table=table)
            cursor.execute(check_query)

            result = cursor.fetchall()

            if(not result or len(result) == 0 or len(result[0]) == 0 or result[0][0] == 0):
                print("ERROR: Table {table} is not initialized or no data present".format(table=table))

            else:
                print("PASS: Check for data existence - The table {table} has {number_of_records} records".format(table=table, number_of_records=result[0][0]))
        
        cursor.close()

        conn.commit()
        conn.close()

    def check_null(self):

        conn = self.obtain_redshift_connector()
        cursor = conn.cursor()

        check_tables_columns_dict = {"state_wise_trend": ["country_name", "latitude", "longitude"]}
        

        for table in check_tables_columns_dict:

            column_list = check_tables_columns_dict[table]
            
            for column in column_list:

                check_query = SqlQueries.sql_queries_dict["check_null"].format(table=table, column=column)
                cursor.execute(check_query)

                result = cursor.fetchall()

                if(not result or len(result) == 0 or len(result[0]) == 0):
                    print("ERROR: Table {table} is not initialized or no data present".format(table=table))

                elif(result[0][0] > 0):
                    print("WARNING: Table {table} contains {number_of_records} null records for column {column}".format(table=table, number_of_records=result[0][0], column=column))

                else:
                    print("PASS: Check for no null data - The column {column} in table {table} has no null records".format(column = column, table=table))
        
        cursor.close()

        conn.commit()
        conn.close()    

    def check_negative(self):

        conn = self.obtain_redshift_connector()
        cursor = conn.cursor()

        check_tables_columns_dict = {"state_wise_trend": ["confirmed", "deaths", "recovered", "active"]}
        

        for table in check_tables_columns_dict:

            column_list = check_tables_columns_dict[table]
            
            for column in column_list:

                check_query = SqlQueries.sql_queries_dict["check_negative"].format(table=table, column=column)
                cursor.execute(check_query)

                result = cursor.fetchall()

                if(not result or len(result) == 0 or len(result[0]) == 0):
                    print("ERROR: Table {table} is not initialized or no data present".format(table=table))

                elif(result[0][0] > 0):
                    print("WARNING: Table {table} contains {number_of_records} negative records for column {column}".format(table=table, number_of_records=result[0][0], column=column))

                else:
                    print("PASS: Check for no negative data - The column {column} in table {table} has no negative records".format(column = column, table=table))
        
        cursor.close()

        conn.commit()
        conn.close()

    def drop_tables(self, drop_tables_list=[]):
        
        if(not drop_tables_list):
            drop_tables_list = ["world_covid", "geocoding_mapping", "state_wise_trend"]

        conn = self.obtain_redshift_connector()
        cursor = conn.cursor()

        for table in drop_tables_list:
            drop_query = SqlQueries.sql_queries_dict["drop_table_query"].format(table=table)
            cursor.execute(drop_query)
        
        cursor.close()

        conn.commit()
        conn.close()




