# import requests as re
import http.client, urllib.parse
import json
import pandas as pd
import ast
import configparser
from plugins.helpers.redshift_helper import RedshiftHelper
from plugins.helpers.sql_queries import SqlQueries

# RedshiftHelper.create_all_tables()

class PositionStack:

	def __init__(self):

		self.config = configparser.RawConfigParser()
		self.config.read('config.cfg')

	def get_lat_lon_list(self):

		'''
		Obtain only those latitude, longitude that do not already exist in geocoding_mapping, 
		to optimize API calls.
		'''

		query = SqlQueries.sql_queries_dict["obtain_lat_lon_list"]
		return RedshiftHelper().execute_select_dataframe(query)

	def call_position_api(self, insert_query_parameters):

		position_stack_api_config = dict(self.config.items('position_stack_api'))
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

	def insert_into_geocoding_mapping(self, insert_query_parameters):

		insert_query_format = SqlQueries.sql_queries_dict["insert_into_geocoding_mapping_query_format"]
		insert_query = insert_query_format.format(col_list = ", ".join(insert_query_parameters.keys()))
		RedshiftHelper().execute_insert(insert_query, tuple(insert_query_parameters.values()))


	def implementor(self):

		"""
		Main function, which fetches the relevant data, calls API, and stores the results in table
		"""
		df = self.get_lat_lon_list()

		for row in df.iterrows():

			insert_query_parameters = {"source_country_name": row[1]["country_name"],
									   "source_latitude" 	: float(row[1]["latitude"]),
									   "source_longitude" 	: float(row[1]["longitude"])
									}

			data = self.call_position_api(insert_query_parameters)

			insert_query_parameters.update({
						"result_latitude" 				: data["latitude"],
						"result_longitude" 				: data["longitude"],
						"result_type" 					: data["type"],
						"result_name" 					: data["name"],
						"result_number" 				: data["number"],
						"result_postal_code" 			: data["postal_code"],
						"result_street"	 				: data["street"],
						"result_confidence" 			: data["confidence"],
						"result_region" 				: data["region"],
						"result_region_code" 			: data["region_code"],
						"result_county" 				: data["county"],
						"result_locality" 				: data["locality"],
						"result_administrative_area" 	: data["administrative_area"],
						"result_neighbourhood" 			: data["neighbourhood"],
						"result_country" 				: data["country"],
						"result_country_code" 			: data["country_code"],
						"result_continent" 				: data["continent"],
						"result_label" 					: data["label"]
						})

			self.insert_into_geocoding_mapping(insert_query_parameters)

			

