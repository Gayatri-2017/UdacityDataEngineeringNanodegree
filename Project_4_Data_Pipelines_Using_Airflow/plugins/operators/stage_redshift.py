from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

'''

Stage Operator
The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. 
The operator creates and runs a SQL COPY statement based on the parameters provided. 
The operator's parameters should specify where in S3 the file is loaded and what is the target table.

The parameters should be used to distinguish between JSON file.
Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

'''

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    
    template_fields = ("s3_key",)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        IGNOREHEADER {}
        DELIMITER '{}'
    """
    
    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # redshift_conn_id=your-connection-name
                 redshift_conn_id='',
                 aws_conn_id='',
                 target_table='',
                 s3_key='',
                 s3_bucket='',
                 delimiter=",",
                 ignore_headers=1,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        
        self.s3_key=s3_key
        self.s3_bucket=s3_bucket
        self.redshift_conn_id=redshift_conn_id
        self.aws_conn_id=aws_conn_id
        self.target_table=target_table
        self.delimiter=delimiter
        self.ignore_headers=ignore_headers

    def execute(self, context):
        self.log.info('StageToRedshiftOperator implementation in progress')
        
        redshift_hook=PostgresHook(self.redshift_conn_id)
        
        aws_hook = AwsHook(self.aws_conn_id)
        credentials = aws_hook.get_credentials()
        
        self.log.info("Clearing data from destination Redshift table")
        redshift_hook.run("DELETE FROM {}".format(self.target_table))
        
        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.target_table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.ignore_headers,
            self.delimiter
        )
        redshift_hook.run(formatted_sql)



