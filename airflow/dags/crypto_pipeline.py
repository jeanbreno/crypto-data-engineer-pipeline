from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="crypto_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    ingest_api = BashOperator(
        task_id="extract_crypto_api",
        bash_command="python /opt/airflow/scripts/extract_api.py"
    )

    ingest_api