import sys
sys.path.append("/Users/apple/Desktop/Udacity/Git_Udacity/UdacityDataEngineeringNanodegree/Capstone_Project")


from plugins.helpers import SqlQueries, RedshiftHelper, PositionStack, GoogleAPI

# # Load data from Google API
GoogleAPI().implementor(load_type='incremental_load',limit=100)
#### GoogleAPI().implementor(load_type='full_load')
# # Create all tables if not exists and copy data
# RedshiftHelper().create_all_tables()
# RedshiftHelper().copy_data_into_tables()
# # Call API for getting state information
# PositionStack().implementor()
# # Insert into statewise trends
# query = SqlQueries.sql_queries_dict["insert_into_state_wise_trend"]
# RedshiftHelper().execute_insert_select(query)
# # Perform Checks
# RedshiftHelper().check_no_data_exists()
# RedshiftHelper().check_null()
# RedshiftHelper().check_negative()