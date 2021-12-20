from google.cloud import bigquery
import boto3

client = bigquery.Client()

filter_condition = " WHERE UPPER(country_name) = 'INDIA'"
    
sql_query = """
    SELECT * 
    FROM `covid-assistant.covid.world_covid` 
    {WHERE}
    LIMIT 100
    """.format(WHERE = filter_condition)

    # 200000
    # 200000
table_df = client.query(sql_query).to_dataframe()

# Converting all columns to string
for column in table_df:
    if (table_df[column].apply(type)==str).any():
        table_df[column] = table_df[column].str.encode('ascii', 'ignore').str.decode('ascii')
        table_df[column] = table_df[column].str.replace('"','')

table = "world_covid-India"
s3_bucket_path = 's3://udacity-capstone-project-gg/world_covid/'

table_df.to_csv(s3_bucket_path+table+".csv")
