from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

with DAG(
    dag_id="crypto_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False,
    tags=["crypto","data-engineering"]
) as dag:

    # ----------------------
    # INGESTION
    # ----------------------

    with TaskGroup("ingestion_layer") as ingestion_layer:
        
        ingest_api_to_raw = BashOperator(
            task_id="extract_crypto_api",
            bash_command="python /opt/airflow/ingestion/extract/extract_api.py"
        )

    # ----------------------
    # BRONZE
    # ----------------------

    with TaskGroup("bronze_layer") as bronze_layer:

        load_raw_to_bronze = BashOperator(
            task_id="load_raw_to_postgres",
            bash_command="python /opt/airflow/ingestion/load/raw_bucket_to_bronze_pg.py"
        )

    # -------------------------
    # DATA QUALITY
    # -------------------------

    with TaskGroup("data_quality_layer") as quality_layer:

        data_quality = BashOperator(
            task_id="data_quality_check",
            bash_command="python /opt/airflow/quality/data_quality_check.py"
        )

    # ----------------------
    # TRANSFORMATIONS (DBT)
    # ----------------------

    with TaskGroup("dbt_transformations") as dbt_layer:

        dbt_build = BashOperator(
            task_id="dbt_build",
            bash_command="cd /opt/airflow/dbt && dbt build --profiles-dir ."
        )

    # ----------------------
    # PIPELINE FLOW
    # ----------------------

    ingestion_layer >> bronze_layer >> quality_layer >> dbt_build