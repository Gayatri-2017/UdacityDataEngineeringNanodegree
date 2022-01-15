import configparser
import sys

config = configparser.RawConfigParser()
config.read('config.cfg')
pwd_config = dict(config.items('present_working_directory'))

sys.path.append(pwd_config["pwd"])

from plugins.helpers import SqlQueries, RedshiftHelper, PositionStack, GoogleAPI

print("Loading data from Google Big Query into S3 buckets")
## For first time ful load, use the following function call
# GoogleAPI().implementor(load_type='full_load')
## Load data from Google API
GoogleAPI().implementor(load_type='incremental_load')

# Drop and Re-Create all tables if not exists and copy data
print("Drop tables from Redshift database if already exist")
RedshiftHelper().drop_tables()

print("Create all tables from Redshift database if not already exist")
RedshiftHelper().create_all_tables()

print("Copy data into Redshift table from S3 bucket")
RedshiftHelper().copy_data_into_tables()

# Call API for getting state information
print("Call the Position Stack API")
PositionStack().implementor()

# Insert into statewise trends
query = SqlQueries.sql_queries_dict["insert_into_state_wise_trend"]
print("Insert data into the Fact table")
RedshiftHelper().execute_insert_select(query)

# Perform Checks
print("Perform checks on the table")
RedshiftHelper().check_no_data_exists()
RedshiftHelper().check_null()
RedshiftHelper().check_negative()