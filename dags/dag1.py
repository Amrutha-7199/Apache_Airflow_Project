from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

from clean import pre_process
from filter import filter_function


#BashOperator
#PythonOperator
#EmailOperator

default_args = {
    "owner" : "airflow",
    "start_date" : datetime(2025,3,8)
}

with DAG(dag_id='test_dag', default_args=default_args, schedule_interval='@daily') as dag:

    #task 1 - chech file
    check_file = BashOperator(
        task_id='check_file',
        bash_command="shasum ~/ip_file/countries.csv",
        retries=2,
        retry_delay=timedelta(seconds=15)
    )

    #task 2 - Preprocess
    pre_process = PythonOperator(
        task_id = 'pre_process',
        python_callable = pre_process
    )

    #task 3 - filter data
    filter_task = PythonOperator(
        task_id = 'filter_data',
        python_callable = filter_function
    )

    #task 4 - Send Email
    email = EmailOperator(
        task_id = 'send_email',
        to = 'xxx@gmail.com',
        subject = 'Daily Report Generated & Report Attached',
        html_content = '<h1> Hello, Your reports are generated successfully, Thanks',
        files = ['/usr/local/airflow/op_file/countries_filtered.csv'],
        cc = ['xxx@gmail.com'] 
    )
    
    check_file >> pre_process >> filter_task >> email