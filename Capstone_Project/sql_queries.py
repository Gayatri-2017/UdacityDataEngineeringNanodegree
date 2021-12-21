
sql_queries_dict = {}

sql_queries_dict.update(
{"obtain_lat_lon_list" : """SELECT DISTINCT
						wc.country_name, 
						wc.latitude,
						wc.longitude
						FROM public.world_covid wc
						LEFT JOIN public.geocoding_mapping gm
							ON wc.latitude = gm.source_latitude
							AND wc.longitude = gm.source_longitude
							AND wc.country_name = gm.source_country_name
						WHERE gm.source_latitude is null 
						OR gm.source_longitude is null 
						OR gm.source_country_name is null;
						"""
,
"insert_into_geocoding_mapping_query_format" : """INSERT INTO public.geocoding_mapping ({col_list}) VALUES (%s, %s, %s, %s, %s, %s, 
%s, %s, %s, %s, %s, %s, 
%s, %s, %s, %s, %s, %s, 
%s, %s, %s);
"""
,
"insert_into_state_wise_trend": """INSERT INTO public.state_wise_trend (id, country_name, state_name,
latitude, longitude, confirmed, deaths, recovered, active, refresh_date) 
WITH latest_world_covid AS 
(SELECT wc.id
, wc.country_name
, gm.state_name
, wc.latitude
, wc.longitude
, wc.confirmed
, wc.deaths
, wc.recovered
, wc.active
, wc.refresh_date
, ROW_NUMBER() OVER (PARTITION BY gm.state_name ORDER BY wc.refresh_date DESC) latest_row,
FROM public.world_covid wc
LEFT JOIN public.geocoding_mapping gm
	ON wc.latitude = gm.source_latitude
	AND wc.longitude = gm.source_longitude
	AND wc.country_name = gm.source_country_name
)
SELECT id
, country_name
, state_name
, latitude
, longitude
, confirmed
, deaths
, recovered
, active
, refresh_date
FROM latest_world_covid
WHERE latest_row = 1
)

"create_geocoding_mapping_query" : """CREATE TABLE IF NOT EXISTS public.geocoding_mapping 
( source_country_name VARCHAR(256)
, source_latitude decimal(10, 6)
, source_longitude decimal(10, 6)
, result_latitude decimal(10, 6)
, result_longitude decimal(10, 6)
, result_type VARCHAR(256)
, result_name VARCHAR(256)
, result_number int
, result_postal_code VARCHAR(16)
, result_street VARCHAR(256)
, result_confidence float
, result_region VARCHAR(256)
, result_region_code VARCHAR(16)
, result_county VARCHAR(256)
, result_locality VARCHAR(256)
, result_administrative_area VARCHAR(256)
, result_neighbourhood VARCHAR(256)
, result_country VARCHAR(256)
, result_country_code VARCHAR(16)
, result_continent VARCHAR(256)
, result_label VARCHAR(256)
);
"""
,
"create_world_covid_query" : """CREATE TABLE IF NOT EXISTS public.world_covid 
( id int not null,
country_name VARCHAR(256) NOT NULL,
state_name VARCHAR(256),
county_code_fips VARCHAR(256),
county_name VARCHAR(256),
latitude decimal(10, 6),
longitude decimal(10, 6),
confirmed bigint,
deaths bigint,
recovered bigint,
active bigint,
refresh_date date,
combined_key VARCHAR(256) NOT NULL,
last_updated timestamp,
incidence_rate decimal(15, 5),
case_fatality_ratio decimal(15, 5)
);
"""
,
"create_state_wise_trend": """CREATE TABLE IF NOT EXISTS public.state_wise_trend 
( id int not null,
country_name VARCHAR(256) NOT NULL,
state_name VARCHAR(256),
latitude decimal(10, 6),
longitude decimal(10, 6),
confirmed bigint,
deaths bigint,
recovered bigint,
active bigint,
refresh_date date
);
"""
,
"copy_world_covid_query" : """COPY public.world_covid 
    FROM 's3://udacity-capstone-project-gg/world_covid/'
    CREDENTIALS
    'aws_access_key_id={aws_access_key_id};aws_secret_access_key={aws_secret_access_key}'
    IGNOREHEADER 1
    FORMAT AS CSV;
    """    
})