<!-- To get query which was executed -->

<!-- #     sql = cur.mogrify(song_select, (row.song, row.artist, row.length)) -->
<!-- #     print("sql = ", sql) -->


# Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.

## Introduction
Sparkify is a Mobile App for Streaming music. It is a startup company and hence would like to plan their strategies and promotions to maximize user retention and reduce churn rate. The company wants to analyze the user and song log data being collected using their mobile application. The analytics team is particularly interested in understanding what songs their users are listening to. Currently, their data resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. 

## Project Description
This project consists of a database schema for the PostgreSQL Database and ETL pipeline for migrating the data from JSON files to RDBMS. The Postgres database is designed to optimize queries on song play analysis. 

# State and justify your database schema design and ETL pipeline.

The database model is a Star Schema consisting of 4 dimension tables: `users`, `songs`, `artists` and `time`, built using the song_data and the log_data and one fact table, `songplays` built using the 4 dimension tables. 

There are multiple decision rationale involved in choosing this datamodel which can be jsutified as follows:

| Decision Made  |  Reasoning behind |
|----------------|-------------------|
| Choice of SQL over NoSQL | The data is structured in the form of JSON files and hence it is fixed. <br>The data size is moderate size and huge. <br>The data can be joined and analyzed using the relational database and joins|
| Choice of Star Schema  |  Multiple tables are involved in the join <br>Efficient to have a fact table with the required metrics and foreign keys from other tables |


Schema for Song Play Analysis
The project includes the following tables.

### Fact Table

`songplays` - records in log data associated with song plays i.e. records with page NextSong

| songplay_id | start_time | user_id | level | song_id | artist_id | session_id | location | user_agent |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |     


### Dimension Tables

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

Running of the project:

Step 1: Create the Database and the tables
Run the Following command in the terminal

`
python create_tables.py
`

Step 2: Run the ETL pipeline to load the data from JSON to Postgres Database

`
python etl.py
`

Optionally, After Step 1, you can view the ETL process in detail for extracting, transforming and loading one JSON file by using `Restart and Run All Cells` options in the `etl.ipynb` Jupyter Notebook
Also, if you want to view the data in individual tables or test the Data Integrity of the songplays dataset, you can `Restart and Run All Cells` in the `test.ipynb` Jupyter Notebook

After using any of these notebooks, make sure to `Restart Kernel` so that the connection to the database is released. 

NOTE: You will not be able to run `test.ipynb`, `etl.ipynb`, or `etl.py` until you have run `create_tables.py` at least once to create the sparkifydb database, which these other files connect to.

[Optional] Provide example queries and results for song play analysis.




