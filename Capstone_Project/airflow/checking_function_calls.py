import sys
sys.path.append("/Users/apple/Desktop/Udacity/Git_Udacity/UdacityDataEngineeringNanodegree/Capstone_Project")


from plugins.helpers import SqlQueries, RedshiftHelper, PositionStack, GoogleAPI

# GoogleAPI().implementor(load_type='incremental_load',limit=100)
# RedshiftHelper().create_all_tables()
# RedshiftHelper().copy_data_into_tables()
# PositionStack().implementor()
query = SqlQueries.sql_queries_dict["insert_into_state_wise_trend"]
RedshiftHelper().execute_insert_select(query)