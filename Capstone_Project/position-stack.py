# import requests as re
import http.client, urllib.parse
import json
import pandas as pd
import ast
import configparser
import redshift_helper

config = configparser.RawConfigParser()
config.read('config.cfg')

def get_lat_lon_list():

	'''
	Obtain only those latitude, longitude that do not already exist in geocoding_mapping, 
	to optimize API calls.
	'''
	sql_queries_config = dict(config.items('sql_queries'))
	query = sql_queries_config["obtain_lat_lon_list"]
	return redshift_helper.execute_select_dataframe(query)

def call_position_api(insert_query_parameters):

	position_stack_api_config = dict(config.items('position_stack_api'))
	API_KEY = position_stack_api_config["api_key"]
	limit = 1

	conn = http.client.HTTPConnection('api.positionstack.com')

	params = urllib.parse.urlencode({
	    'access_key': API_KEY,
	    'query': '{latitude},{longitude}'.format(latitude=insert_query_parameters["source_latitude"], 
	    										 longitude=insert_query_parameters["source_longitude"]),
	    'limit': limit
	    })

	conn.request('GET', '/v1/reverse?{}'.format(params))

	res = conn.getresponse()	
	return json.loads(res.read().decode('utf-8'))["data"][0]

def format_input(input_str, is_string=True):
	if input_str:
		if is_string:
			return "'" + input_str + "'"
		else:
			return str(input_str)
	else:
			return str("null")			

def insert_into_geocoding_mapping(insert_query_parameters):

	sql_queries_config = dict(config.items('sql_queries'))
	insert_query_format = sql_queries_config["insert_into_geocoding_mapping_query_format"]
	insert_query = insert_query_format.format(col_list = ", ".join(insert_query_parameters.keys()))

	print(insert_query)

	redshift_helper.execute_insert(insert_query, tuple(insert_query_parameters.values()))
	

df = get_lat_lon_list()

i = 0
for row in df.iterrows():

	i += 1
	if i == 2:
		break

	insert_query_parameters = {"source_country_name": format_input(row[1]["country_name"]),
							   "source_latitude" 	: format_input(row[1]["latitude"], False),
							   "source_longitude" 	: format_input(row[1]["longitude"], False)
							}

	data = call_position_api(insert_query_parameters)

	insert_query_parameters.update({
				"result_latitude" 				: format_input(data["latitude"], False),
				"result_longitude" 				: format_input(data["longitude"], False),
				"result_type" 					: format_input(data["type"]),
				"result_name" 					: format_input(data["name"]),
				"result_number" 				: format_input(data["number"], False),
				"result_postal_code" 			: format_input(data["postal_code"]),
				"result_street"	 				: format_input(data["street"]),
				"result_confidence" 			: format_input(data["confidence"], False),
				"result_region" 				: format_input(data["region"]),
				"result_region_code" 			: format_input(data["region_code"]),
				"result_county" 				: format_input(data["county"]),
				"result_locality" 				: format_input(data["locality"]),
				"result_administrative_area" 	: format_input(data["administrative_area"]),
				"result_neighbourhood" 			: format_input(data["neighbourhood"]),
				"result_country" 				: format_input(data["country"]),
				"result_country_code" 			: format_input(data["country_code"]),
				"result_continent" 				: format_input(data["continent"]),
				"result_label" 					: format_input(data["label"])
				})

	insert_into_geocoding_mapping(insert_query_parameters)

	

