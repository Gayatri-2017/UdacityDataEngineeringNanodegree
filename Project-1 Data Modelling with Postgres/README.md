To get query which was executed

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

Project Template
To get started with the project, go to the workspace on the next page, where you'll find the project template files. You can work on your project and submit your work through this workspace. Alternatively, you can download the project template files from the Resources folder if you'd like to develop your project locally.

In addition to the data files, the project workspace includes six files:

test.ipynb displays the first few rows of each table to let you check your database.
create_tables.py drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.
etl.ipynb reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
etl.py reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.
sql_queries.py contains all your sql queries, and is imported into the last three files above.
README.md provides discussion on your project.
Project Steps
Below are steps you can follow to complete the project:

Create Tables
Write CREATE statements in sql_queries.py to create each table.
Write DROP statements in sql_queries.py to drop each table if it exists.
Run create_tables.py to create your database and tables.
Run test.ipynb to confirm the creation of your tables with the correct columns. Make sure to click "Restart kernel" to close the connection to the database after running this notebook.
Build ETL Processes
Follow instructions in the etl.ipynb notebook to develop ETL processes for each table. At the end of each table section, or at the end of the notebook, run test.ipynb to confirm that records were successfully inserted into each table. Remember to rerun create_tables.py to reset your tables before each time you run this notebook.

Build ETL Pipeline
Use what you've completed in etl.ipynb to complete etl.py, where you'll process the entire datasets. Remember to run create_tables.py before running etl.py to reset your tables. Run test.ipynb to confirm your records were successfully inserted into each table.

Document Process
Do the following steps in your README.md file.

Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
State and justify your database schema design and ETL pipeline.
[Optional] Provide example queries and results for song play analysis.
Here's a guide on Markdown Syntax.

NOTE: You will not be able to run test.ipynb, etl.ipynb, or etl.py until you have run create_tables.py at least once to create the sparkifydb database, which these other files connect to.


[Optional] Provide example queries and results for song play analysis.

