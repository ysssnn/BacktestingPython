from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from Moyenne_mobiles_par_H import run_backtest


default_args = {
    'owner': 'yassine',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='backtest_moyennes_mobiles_par_H',
    start_date=datetime(2025, 12, 10),
    schedule_interval='*/30 * * * *', 
    default_args=default_args,
    catchup=False
) as dag:

    run_backtest_task = PythonOperator(
        task_id='run_backtest_ma',
        python_callable=run_backtest
    )

