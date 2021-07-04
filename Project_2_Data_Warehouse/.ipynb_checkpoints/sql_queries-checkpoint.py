import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN = config.get("IAM_ROLE","ARN")
LOG_DATA = config.get('S3','LOG_DATA')
LOG_JSONPATH = config.get('S3','LOG_JSONPATH')
SONG_DATA = config.get('S3','SONG_DATA')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
staging_events_table_create= ("""
CREATE TABLE staging_events (
artist text,
auth text,
firstName text,
gender text,
itemInSession int,
lastName text,
length decimal,
level text,
location text,
method text,
page text,
registration decimal,
sessionId int,
song text,
status int,
ts timestamp,
userAgent text,
userId int);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
num_songs int,
artist_id text,
artist_latitude decimal,
artist_longitude decimal,
artist_location text,
artist_name text,
song_id text,
title text, 
duration decimal,
year int
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays 
(songplay_id INT IDENTITY(0,1) PRIMARY KEY, 
start_time timestamp,
user_id int, 
level text, 
song_id text,
artist_id text, 
session_id int, 
location text, 
user_agent text);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(user_id int PRIMARY KEY, 
first_name text NOT NULL, 
last_name text NOT NULL, 
gender text,
level text);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs 
(song_id text PRIMARY KEY, 
title text NOT NULL, 
artist_id text NOT NULL, 
year int, 
duration decimal);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists 
(artist_id text PRIMARY KEY, 
name text NOT NULL, 
location text, 
latitude decimal, 
longitude decimal);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time 
(start_time timestamp PRIMARY KEY, 
hour int, 
day int, 
week int, 
month int, 
year int, 
weekday int);
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events from 's3://udacity-dend/log_data'
credentials 'aws_iam_role={}'
json {} 
region 'us-west-2'
timeformat as 'epochmillisecs';
""").format(ARN, LOG_JSONPATH)

staging_songs_copy = ("""
copy staging_songs from 's3://udacity-dend/song_data/A/A'
credentials 'aws_iam_role={}'
json 'auto' 
region 'us-west-2';
""").format(ARN)

# FINAL TABLES
songplay_table_insert = ("""
INSERT INTO songplays 
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DATE(se.ts),
se.userId as user_id,
se.level as level,
ss.song_id,
ss.artist_id,
se.sessionId as session_id,
se.location,
se.userAgent as user_agent
FROM staging_songs ss,
staging_events se
WHERE ss.title = se.song 
AND ss.artist_name = se.artist 
AND ss.duration = se.length
AND se.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users 
(user_id, first_name, last_name, gender, level) 
SELECT 
se.userId as user_id,
se.firstName as first_name,
se.lastName as last_name,
se.gender,
se.level
FROM staging_events se
WHERE se.page = 'NextSong'
""")

song_table_insert = ("""
INSERT INTO songs 
(song_id, title, artist_id, year, duration) 
SELECT 
song_id, 
title, 
artist_id, 
year, 
duration
FROM staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists 
(artist_id, name, location, latitude, longitude) 
SELECT 
artist_id, 
artist_name as name, 
artist_location as location, 
artist_latitude as latitude, 
artist_longitude as longitude
FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time 
(start_time, hour, day, week, month, year, weekday) 
SELECT 
se.ts as start_time,
EXTRACT(hour from se.ts) as hour,
EXTRACT(day from se.ts) as day,
EXTRACT(week from se.ts) as week,
EXTRACT(month from se.ts) as month,
EXTRACT(year from se.ts) as year,
EXTRACT(dow from se.ts) as weekday
FROM staging_events se
WHERE se.page = 'NextSong'
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
