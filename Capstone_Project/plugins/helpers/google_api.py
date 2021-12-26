from google.cloud import bigquery
import boto3

class GoogleAPI:
    def get_bq_client(self):
        return bigquery.Client()

    def full_load_query(self, limit):    

        return """
            SELECT * 
            FROM `covid-assistant.covid.world_covid` 
            LIMIT {limit}
            """.format(limit=limit)

            # 200000
            # 200000

    def incremental_load_query(self, limit):

        """
        Currently functions same as full_load. 
        Ideally, it should find out the max updated_date from world_covid table.
        And fetch data from Google API greater than this max updated date
        TODO: figure out how to store incremental data into s3
        """
        return """
        SELECT * 
        FROM `covid-assistant.covid.world_covid` 
        LIMIT {limit}
        """.format(limit=limit)

    def get_data_from_bq(self, load_type, limit):

        if(load_type=='full_load'):
            sql_query = self.full_load_query(limit)
        else:        
            # Defaulting to incremental load
            sql_query = self.incremental_load_query(limit)
        
        client = self.get_bq_client()
        return client.query(sql_query).to_dataframe()

    def format_df(self, df):

        """
        Clear the formatting
        """
        for column in df:
            if (df[column].apply(type)==str).any():
                df[column] = df[column].str.encode('ascii', 'ignore').str.decode('ascii')
                df[column] = df[column].str.replace('"','')

        return df            

    def save_df_to_s3(self, df):

        table = "world_covid"
        s3_bucket_path = 's3://udacity-capstone-project-gg/world_covid/'

        df.to_csv(s3_bucket_path+table+".csv")


    def implementor(self, load_type='incremental_load',
                    limit=100):

        df = self.format_df(self.get_data_from_bq(load_type=load_type, limit=limit))        
        self.save_df_to_s3(df)
        