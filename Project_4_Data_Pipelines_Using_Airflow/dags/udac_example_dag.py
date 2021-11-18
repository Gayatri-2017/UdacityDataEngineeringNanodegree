from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False, # The DAG does not have dependencies on past runs
    'retries': 3, # On failure, the task are retried 3 times
    'retry_delay': timedelta(minutes=5), # Retries happen every 5 minutes
    'email_on_retry': False, # Do not email on retry
    }

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          max_active_runs=1,
          catchup=False # Catchup is turned off
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# Loading Staging Data from S3 to Redshift
events_json_paths='s3://udacity-dend/log_json_path.json'
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id='redshift',
    aws_conn_id='aws_credentials',
    target_table='staging_events',
    s3_bucket='udacity-dend',
#     s3_key='log_data/{execution_date.year}/{execution_date.month}/{ds}-events.json'
    s3_key='log_data/2018/11/2018-11-01-events.json',
    json_paths=events_json_paths
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id='redshift',
    aws_conn_id='aws_credentials',
    target_table='staging_events',
    s3_bucket='udacity-dend',
    s3_key='song_data',
#     s3_key='song_data/A/A/A',
    json_paths=''
)

# Loading Fact Table using Staging Tables

insert_table_format = 'INSERT INTO public.{} '

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=(insert_table_format + SqlQueries.songplay_table_insert).format("songplays"),
    target_table='songplays',
    truncate=False
)

# Loading Dimension Tables using Staging Tables

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=(insert_table_format + SqlQueries.user_table_insert).format("users"),
    target_table='users',
    truncate=True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=(insert_table_format + SqlQueries.song_table_insert).format("songs"),
    target_table='songs',
    truncate=True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=(insert_table_format + SqlQueries.artist_table_insert).format("artists"),
    target_table='artists',
    truncate=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=(insert_table_format + SqlQueries.time_table_insert).format("time"),
    target_table='time',
    truncate=True
)

# Performing Data Quality Checks
quality_check_query = "SELECT count(*) FROM public.{}"
not_expected_value = 0
tables_list = ["users","songs","artists","time","songplays"]
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=quality_check_query,
    check_table_list=tables_list,
    not_expected_value=not_expected_value
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Defining the Task Order in DAG
start_operator >> stage_events_to_redshift >> load_songplays_table 
start_operator >> stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_song_dimension_table >> run_quality_checks
load_songplays_table >> load_user_dimension_table >> run_quality_checks
load_songplays_table >> load_artist_dimension_table >> run_quality_checks
load_songplays_table >> load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator