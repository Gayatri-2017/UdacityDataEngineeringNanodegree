from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 sql_stmt='',
                 target_table='',
                 truncate=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id=redshift_conn_id
        self.sql_stmt=sql_stmt
        self.target_table=target_table
        self.truncate=truncate

    def execute(self, context):
        self.log.info('LoadDimensionOperator implementation completed')
        
        redshift_hook = PostgresHook(self.redshift_conn_id)
        if(self.truncate):
            self.log.info('Truncating contents of {} table'.format(self.target_table))
            truncate_query = "DELETE FROM public.{}".format(self.target_table)
            redshift_hook.run(truncate_query)
            
        self.log.info('Inserting data into {} table'.format(self.target_table))
        redshift_hook.run(self.sql_stmt)
        
        
