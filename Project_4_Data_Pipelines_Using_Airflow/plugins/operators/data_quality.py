from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 sql_stmt='',
                 check_table_list=[],
                 not_expected_value=None,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.sql_stmt=sql_stmt
        self.check_table_list=check_table_list
        self.not_expected_value=not_expected_value

    def execute(self, context):
        self.log.info('DataQualityOperator implementation completed')
        
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        error_stmt = "\n"
        for table in self.check_table_list:
            
            log_stmt = "Starting Data Quality Checks for {} table".format(table)
            
            records = redshift_hook.get_records(self.sql_stmt.format(table))
            if(records is None or len(records) < 1 or len(records[0]) < 1 ):
                error_stmt += "Data Quality Check 1 Failed for {} table. No records were returned for the quality check query\n".format(table)
                
                
            elif(records[0][0] == self.not_expected_value):
                error_stmt += "Data Quality Check 2 Failed for {} table. No records present in the {} table\n".format(table, table)
            
            else:
                log_stmt = "Data Quality Checks Passed for {} table. The {} table contains {} records".format(table, table, records[0][0])
                self.log.info(log_stmt)
        
        self.log.info("Data Quality Checks complete for all tables") 
        
        if(error_stmt):
            self.log.error(error_stmt)
            raise ValueError(error_stmt)
                
                
        
        
        
        