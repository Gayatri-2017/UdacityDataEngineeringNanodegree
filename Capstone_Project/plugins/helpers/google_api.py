from google.cloud import bigquery
import boto3
from datetime import datetime
# import glob
# import os

class GoogleAPI:
    def get_bq_client(self):
        return bigquery.Client()

    def full_load_query(self, limit):    

        if limit:
            return """
                SELECT * 
                FROM `covid-assistant.covid.world_covid` 
                LIMIT {limit}
                """.format(limit=limit)
        else:
             return """
                SELECT * 
                FROM `covid-assistant.covid.world_covid` 
                """ 

            # 200000
            # 200000

    def get_last_updated_date(self):

        s3resource = boto3.resource('s3') 
        files = list(s3resource.Bucket('udacity-capstone-project-gg').objects.filter(Prefix='world_covid/'))

        files_list = [file.key.split('/')[-1] for file in files]
        files_list.sort()

        if (len(files_list)) > 1:
            return files_list[-1].split(".csv")[0]
        else:
            return '2020-01-01'

    def get_today_date(self):

        return datetime.today().strftime('%Y-%m-%d')

    def incremental_load_query(self, limit):

        """
        Currently functions same as full_load. 
        Ideally, it should find out the max updated_date from world_covid table.
        And fetch data from Google API greater than this max updated date
        TODO: figure out how to store incremental data into s3
        """

        last_date = self.get_last_updated_date()

        if limit:
            return """
            SELECT * 
            FROM `covid-assistant.covid.world_covid` 
            WHERE last_updated > '{last_date}'
            LIMIT {limit}
            """.format(limit=limit, last_date=last_date)
        else:
            return """
            SELECT * 
            FROM `covid-assistant.covid.world_covid` 
            WHERE last_updated > '{last_date}'
            """.format(last_date=last_date)           

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

        # table = "world_covid"
        s3_bucket_path = 's3://udacity-capstone-project-gg/world_covid/'


        # df.to_csv(s3_bucket_path+self.get_today_date()+".csv")
        df.to_parquet(s3_bucket_path+self.get_today_date()+".gzip", compression='gzip')


    def implementor(self, limit=None, load_type='incremental_load'):

        df = self.format_df(self.get_data_from_bq(load_type=load_type, limit=limit))        
        self.save_df_to_s3(df)
        