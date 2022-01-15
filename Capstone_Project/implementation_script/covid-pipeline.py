from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from helpers import SqlQueries, RedshiftHelper, PositionStack, GoogleAPI

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    'covid-pipeline',
    default_args=default_args,
    description='A DAG to load and transform world-covid data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 12, 1),

) as dag:
    
    start = DummyOperator(task_id='start')

    get_data_from_google_bq = PythonOperator(
                                            task_id = "get_data_from_google_bq"
                                            , python_callable=my_function,
        )

    end = DummyOperator(task_id='end')
    
    start >> get_data_from_google_bq >> end
