# Introduction
Sparkify is a Mobile App for Streaming music. It is a startup company which aims to improve it's user retention and cater to the needs and preferences of the user. The company wants to analyze the user and song log data which is collected using their mobile application. The analytics team is particularly interested in understanding what songs their users are listening to. Currently, their data resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. 

# Project Description
Sparkify is a rapidly growing Startup. This indirectly implies a growing user base and song base!
In this project, we build a ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables.
The final tables in S3 are stored in Parquet format with appropriate partitioning, wherever feasible, for faster Analytical processing. 

# DataBase Schema
The database model is a Star Schema consisting of 4 dimension tables: `users`, `songs`, `artists` and `time`.
These tables are built using the `song_data` and the `log_data`.
We then have one fact table, `songplays` built using the 4 dimension tables. 

There are multiple decision rationale involved in choosing this datamodel which can be jsutified as follows:

| Decision Made  |  Reasoning behind |
|----------------|-------------------|
| Choice of AWS S3 with Spark | Spark works best with Partitioned Data Store, as it can work and process efficiently.  The data is structured in the form of JSON files and hence it is fixed. <br>The data size is moderate size and huge. <br>The data can be joined and analyzed using the relational database and joins|
| Choice of Star Schema  |  Multiple tables are involved in the join <br>Efficient to have a fact table with the required metrics and foreign keys from other tables |


Schema for Song Play Analysis
The project includes the following tables.

## Staging Tables

These tables are used to load the data directly from S3 buckets to table, without any transformations

`staging_events` - To store data from Log data JSON files to staging_events table.

| artist | auth | firstName |	gender | itemInSession | lastName |	length | level | location |	method | page |	registration |	sessionId |	song |	status |	ts |	userAgent |	userId |
| ---- | ---- | ---- |	---- | ---- | ---- |	---- | ---- | ---- |	---- | ---- |	---- |	---- |	---- |	---- |	---- |	---- |	---- |

`staging_songs` - To store data from Song data JSON files to staging_songs table.

| num_songs |	artist_id |	artist_latitude |	artist_longitude |	artist_location |	artist_name |	song_id |	title |	duration |	year |
| ---- |	---- |	---- |	---- |	---- |	---- |	---- |	---- |	---- |	---- |

## Fact Table

`songplays` - records in log data associated with song plays i.e. records with page NextSong

| songplay_id | start_time | user_id | level | song_id | artist_id | session_id | location | user_agent |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |     


## Dimension Tables

`users` - users in the app

| user_id | first_name | last_name | gender | level |
| ---- | ---- | ---- | ---- | ---- |

`songs` - songs in music database

| song_id | title | artist_id | year | duration |
| ---- | ---- | ---- | ---- | ---- |

`artists` - artists in music database

| artist_id | name | location | latitude | longitude |
| ---- | ---- | ---- | ---- | ---- |

`time` - timestamps of records in songplays broken down into specific units

| start_time | hour | day | week | month | year | weekday |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | 


# Description of the files in this Project

`dwh.cfg`
Contains configuration details for connecting to Redshift cluster. 

`create_tables.py` 
Contains script to delete existing tables and create new tables in the database. 
It can be used to reset the tables before running the ETL scripts.

`etl.py` 
Reads and processes files from song_data and log_data and loads them into the Database tables. 

`sql_queries.py` 
Contains all the sql queries required in this Project

`README.md` 
Contains documentation and information about the Project

# Running of the project:

Step 0: Start the Redshift cluster and enter the credentials in `dwh.cfg` configuration

Step 1: Create the Database and the tables
Run the Following command in the terminal

`
python create_tables.py
`

Step 2: Run the ETL pipeline to load the data from JSON to Postgres Database

`
python etl.py
`

# Some possible Analytical Queries:
```
Top 5 most preferred locations¶
```

```
query = """
SELECT location, count(DISTINCT user_id) as user_count
FROM songplays sp
WHERE song_id is not null and artist_id is not null
GROUP BY location
ORDER BY count(DISTINCT user_id) DESC
"""

%sql $query

```
