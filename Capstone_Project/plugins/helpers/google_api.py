from google.cloud import bigquery
import boto3
from datetime import datetime
import configparser


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

    def get_last_updated_date(self):

        config = configparser.RawConfigParser()
        config.read('config.cfg')

        s3_details_config = dict(config.items('s3_details'))
        bucket_name = s3_details_config["bucket_name"]
        prefix = s3_details_config["prefix"]
        file_ext_with_dot = s3_details_config["file_ext_with_dot"]
        start_date = s3_details_config["start_date"]

        s3resource = boto3.resource('s3')     
        files = list(s3resource.Bucket(bucket_name).objects.filter(Prefix=prefix))

        files_list = [file.key.split('/')[-1] for file in files]
        files_list.sort()

        if (len(files_list)) > 1:
            return files_list[-1].split(file_ext_with_dot)[0]
        else:
            return start_date

    def get_today_date(self):

        return datetime.today().strftime('%Y-%m-%d')

    def incremental_load_query(self, limit):

        """
        Find the last load date, based on file name, and load data after that load date till today. 
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

        config = configparser.RawConfigParser()
        config.read('config.cfg')

        s3_details_config = dict(config.items('s3_details'))
        s3_bucket_path = s3_details_config["s3_bucket_path"]
        file_ext = s3_details_config["file_ext"]
        file_ext_with_dot = s3_details_config["file_ext_with_dot"]

        df.to_parquet(s3_bucket_path+self.get_today_date()+file_ext_with_dot, compression=file_ext)


    def implementor(self, limit=None, load_type='incremental_load'):

        df = self.format_df(self.get_data_from_bq(load_type=load_type, limit=limit))        
        self.save_df_to_s3(df)
        