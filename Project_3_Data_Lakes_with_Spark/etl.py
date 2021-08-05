import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

# Extra imports
from pyspark.sql.types import TimestampType
from pyspark.sql.functions import monotonically_increasing_id, dayofweek

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['KEYS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['KEYS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()

    # Changing the logging level to see only Error logs on Console
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def process_song_data(spark, input_data, output_data):
    '''
    The method creates songs_table and artists_table using the song_data in S3.
    '''
    
    
    # get filepath to song data file
    song_data = input_data + config['FILE_PATHS']['SONG_DATA_PATH']
    
    # read song data file
    song_df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = song_df.selectExpr("song_id", "title", "artist_id", "year", "duration").distinct()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write \
               .mode("overwrite") \
               .partitionBy("year","artist_id") \
               .parquet(output_data + "songs_table/")

    # extract columns to create artists table
    orig_col_list = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
    reqd_col_list = ["artist_id", "name", "location", "latitude", "longitude"]
    exprs = ['{} as {}'.format(orig_col_list[i], reqd_col_list[i]) for i in range(len(orig_col_list)) ]
    
    artists_table = song_df.selectExpr(*exprs).distinct()
    
    # write artists table to parquet files
    artists_table.write \
                 .mode("overwrite") \
                 .parquet(output_data + "artists_table/")


def process_log_data(spark, input_data, output_data):
    '''
    The method creates users_table, time_table and songplays_table using the song_data in S3.
    '''
    
    # get filepath to log data file
    log_data = input_data + config['FILE_PATHS']['LOG_DATA_PATH']

    # read log data file
    log_df = spark.read.json(log_data)
    
    # filter by actions for song plays
    log_df = log_df.where('page = "NextSong" ')

    # extract columns for users table    
    orig_col_list = ["userId", "firstName", "lastName", "gender", "level"]
    reqd_col_list = ["user_id", "first_name", "last_name", "gender", "level"]
    exprs = ['{} as {}'.format(orig_col_list[i], reqd_col_list[i]) for i in range(len(orig_col_list)) ]
    users_table = log_df.selectExpr(*exprs).distinct()
    
    # write users table to parquet files
    users_table.write \
               .mode("overwrite") \
               .parquet(output_data + "users_table/")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda ts: datetime.fromtimestamp(ts), TimestampType())
    log_df = log_df.withColumn('timestamp', get_timestamp(col("ts")/1000))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x), TimestampType())
    log_df = log_df.withColumn('start_time', get_datetime(col("ts")/1000))
    
    log_df = log_df.withColumn("hour", hour("timestamp")) \
                    .withColumn("dayofmonth", dayofmonth("timestamp")) \
                    .withColumn("weekofyear", weekofyear("timestamp")) \
                    .withColumn("month", month("timestamp")) \
                    .withColumn("year", year("timestamp")) \
                    .withColumn("weekday", dayofweek("timestamp"))
    # extract columns to create time table
    time_table = log_df.select("start_time", "hour", "dayofmonth", "weekofyear", "month", "year", "weekday").distinct()
    
    # write time table to parquet files partitioned by year and month
    time_table.write \
            .mode("overwrite") \
            .partitionBy("year","month") \
            .parquet(output_data + "time_table/")

    # read in song data to use for songplays table
    spark.read.parquet(output_data + "songs_table/").createOrReplaceTempView("songs_table")
    spark.read.parquet(output_data + "artists_table/").createOrReplaceTempView("artists_table")
    
    query_1 = """
    SELECT song_id, 
           at.artist_id, 
           title, 
           at.name as artist_name, 
           duration
    FROM songs_table st, artists_table at
    WHERE st.artist_id = at.artist_id
    """
    song_df = spark.sql(query_1)
 

    # extract columns from joined song and log datasets to create songplays table 
    conditions = [song_df.title == log_df.song, song_df.artist_name == log_df.artist, song_df.duration == log_df.length]
    songplays_table = song_df.join(other = log_df, \
                                     on=conditions) \
                                .selectExpr("start_time as start_time", \
                                        "userId as user_id", \
                                        "level as level", \
                                        "song_id as song_id", \
                                        "artist_id as artist_id", \
                                        "sessionId as sessionId", \
                                        "location as location", \
                                        "userAgent as userAgent", \
                                        "year as year", \
                                        "month as month") \
                                .distinct() \
                                .withColumn("songplay_id", monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write \
                    .mode("overwrite") \
                    .partitionBy("year","month") \
                    .parquet(output_data + "songplays_table/")


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-output/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
