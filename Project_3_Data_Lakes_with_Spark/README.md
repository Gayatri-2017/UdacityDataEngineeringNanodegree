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
| Choice of AWS S3 with Spark | Spark works best with Partitioned Data Store, as it can process efficiently and parallely in chunks. <br>S3 gives a permanent storage independent of the EMR cluster. Hence the data is always available in S3 buckets. Also the storage cost of S3 is less than using the HDFS in EMR and keeping the cluster running all the time.|
| Choice of Star Schema  |  Multiple tables are involved in the join <br>Efficient to have a fact table with the required metrics and foreign keys from other tables |


Schema for Song Play Analysis
The project includes the following tables.

## Fact Table

`songplays` - records in log data associated with song plays i.e. records with page NextSong

| songplay_id | start_time | user_id | level | song_id | artist_id | session_id | location | user_agent |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |     

(The table is stored in Parquet format partitioned by year and month)

## Dimension Tables

`users` - users in the app

| user_id | first_name | last_name | gender | level |
| ---- | ---- | ---- | ---- | ---- |

(The table is stored in Parquet format)

`songs` - songs in music database

| song_id | title | artist_id | year | duration |
| ---- | ---- | ---- | ---- | ---- |

(The table is stored in Parquet format partitioned by year and artist_id)

`artists` - artists in music database

| artist_id | name | location | latitude | longitude |
| ---- | ---- | ---- | ---- | ---- |

(The table is stored in Parquet format)

`time` - timestamps of records in songplays broken down into specific units

| start_time | hour | day | week | month | year | weekday |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | 

(The table is stored in Parquet format partitioned by year and month)

# Description of the files in this Project

`dl.cfg`
Contains AWS credentials details for connecting to AWS. Also, it contains the Log and songs directory path. 

`etl.py` 
Reads and processes files from song_data and log_data and loads them into S3 in Parquet Format. 

`README.md` 
Contains documentation and information about the Project

# Running of the project:

Step 0: Enter the AWS credentials in `dl.cfg` configuration file.

Step 1: Run the ETL pipeline to load the JSON data in S3 into Analytical tables stored as Parquet in S3 bucket.

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
