source_country_name
										, source_latitude
										, source_longitude
										, result_latitude
										, result_longitude
										, result_type
										, result_name
										, result_number
										, result_postal_code
										, result_street
										, result_confidence
										, result_region
										, result_region_code
										, result_county
										, result_locality
										, result_administrative_area
										, result_neighbourhood
										, result_country 
										, result_country_code
										, result_continent
										, result_label


	# result_latitude = data["latitude"]
	# result_longitude = data["longitude"]
	# result_type = data["type"]
	# result_name = data["name"]
	# result_number = data["number"]
	# result_postal_code = data["postal_code"]
	# result_street = data["street"]
	# result_confidence = data["confidence"]
	# result_region = data["region"]
	# result_region_code = data["region_code"]
	# result_county = data["county"]
	# result_locality = data["locality"]
	# result_administrative_area = data["administrative_area"]
	# result_neighbourhood = data["neighbourhood"]
	# result_country = data["country"]
	# result_country_code = data["country_code"]
	# result_continent = data["continent"]
	# result_label = data["label"]

	# print(region)

	{
  "data": [
    {
      "latitude": 40.763841,
      "longitude": -73.972972,
      "type": "venue",
      "distance": 0,
      "name": "Apple Store",
      "number": "767",
      "postal_code": "10153",
      "street": "5th Avenue",
      "confidence": 1,
      "region": "New York",
      "region_code": "NY",
      "county": "New York County",
      "locality": "New York",
      "administrative_area": null,
      "neighbourhood": "Midtown East",
      "country": "United States",
      "country_code": "USA",
      "continent": "North America",
      "label": "Apple Store, New York, NY, USA"
    }
  ]
}


query = """
select 
country_name,
state_name,
county_code_fips,
county_name,
latitude,
longitude
from public.world_covid
limit 10
"""
df = execute_select_dataframe(query)
print(df.head(10))



    	 # ', '.join("'{0}'".format(col) for col in insert_query_parameters.values()))											 

# print("result_label = ", result_label)

# Make a list of unique latitude and longitude for api call 
# # row[1]["id"]
# , row[1]["Latitude"] as inquiry_latitude
# , row[1]["longitude"] as inquiry_longitude
# data["data"][0]["......."] as result_......

# insert into table addresses

# create tables, state_wise_covid, country_wise_covid, 
# have two filters, recovered, deaths in tableau



insert_query_parameters = {"source_country_name":format_input(row[1]["country_name"]),
							   "source_latitude" 	: str(row[1]["latitude"]),
							   "source_longitude" 	: str(row[1]["longitude"])
							}

	data = call_position_api(insert_query_parameters)

	insert_query_parameters.update({
				"result_latitude" 				: str(data["latitude"]),
				"result_longitude" 				: str(data["longitude"]),
				"result_type" 					: "'" + data["type"] 						+ "'",
				"result_name" 					: "'" + data["name"] 						+ "'",
				"result_number" 				: str(data["number"]),
				"result_postal_code" 			: "'" + str(data["postal_code"])			+ "'",
				"result_street"	 				: "'" + str(data["street"]) 				+ "'",
				"result_confidence" 			: str(data["confidence"]),
				"result_region" 				: "'" + str(data["region"]) 				+ "'",
				"result_region_code" 			: "'" + str(data["region_code"])			+ "'",
				"result_county" 				: "'" + str(data["county"]) 				+ "'",
				"result_locality" 				: "'" + str(data["locality"]) 				+ "'",
				"result_administrative_area" 	: "'" + str(data["administrative_area"]) 	+ "'",
				"result_neighbourhood" 			: "'" + str(data["neighbourhood"]) 			+ "'",
				"result_country" 				: "'" + str(data["country"]) 				+ "'",
				"result_country_code" 			: "'" + str(data["country_code"]) 			+ "'",
				"result_continent" 				: "'" + str(data["continent"]) 				+ "'",
				"result_label" 					: "'" + str(data["label"]) 					+ "'"
				})