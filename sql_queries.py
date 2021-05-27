# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (songplay_id text, start_time time, user_id int, level text, song_id text, artist_id text, session_id int, location text, user_agent text);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(user_id int, first_name text, last_name text, gender text, level text);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (song_id text, title text, artist_id text, year int, duration decimal);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (artist_id text, name text, location text, latitude decimal, longitude decimal);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (start_time time, hour int, day int, week int, month int, year int, weekday text);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s)
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

# Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.

song_select = ("""
SELECT s.song_id, a.artist_id 
FROM songs s JOIN artists a ON s.artist_id = a.artist_id
WHERE s.title = %s AND a.name = %s AND s.duration = %s
""")

# 
# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]