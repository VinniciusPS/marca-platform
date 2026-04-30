# airflow/dags/google_trends_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from services.google_trends import GoogleTrendsService
from services.postgres import PostgresService
from services.load_control import LoadControlService
from repository.connection import get_engine

DATASET_NAME = "google_trends"

KEYWORD_GROUPS = {...}

def start_load(**context):
    engine = get_engine()
    svc = LoadControlService(engine)

    load_id = svc.start_load(DATASET_NAME)

    context["ti"].xcom_push(key="load_id", value=load_id)


def extract(**context):
    engine = get_engine()
    load_svc = LoadControlService(engine)

    last_watermark = load_svc.get_last_successful_watermark(DATASET_NAME)

    timeframe = "today 1-m" if not last_watermark else "now 1-d"

    trends = GoogleTrendsService()
    df = trends.fetch(KEYWORD_GROUPS, timeframe)

    context["ti"].xcom_push(key="dataframe", value=df.to_json())
    context["ti"].xcom_push(key="rows_extracted", value=len(df))


def load(**context):
    import pandas as pd

    engine = get_engine()
    pg = PostgresService(engine)

    df_json = context["ti"].xcom_pull(key="dataframe")
    df = pd.read_json(df_json)

    pg.upsert_batch(df)

    context["ti"].xcom_push(key="rows_loaded", value=len(df))
    context["ti"].xcom_push(key="last_extracted_at", value=str(df["date"].max()))


def finish_success(**context):
    engine = get_engine()
    svc = LoadControlService(engine)

    load_id = context["ti"].xcom_pull(key="load_id")
    rows_extracted = context["ti"].xcom_pull(key="rows_extracted")
    rows_loaded = context["ti"].xcom_pull(key="rows_loaded")
    last_extracted_at = context["ti"].xcom_pull(key="last_extracted_at")

    svc.finish_load(
        load_id=load_id,
        status="success",
        rows_extracted=rows_extracted,
        rows_loaded=rows_loaded,
        last_extracted_at=last_extracted_at
    )


def finish_failure(context):
    engine = get_engine()
    svc = LoadControlService(engine)

    load_id = context["ti"].xcom_pull(key="load_id")

    svc.finish_load(
        load_id=load_id,
        status="failed",
        error_message="Pipeline failed"
    )


with DAG(
    dag_id="google_trends_controlled_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="start_load",
        python_callable=start_load,
        provide_context=True
    )

    t2 = PythonOperator(
        task_id="extract",
        python_callable=extract,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id="load",
        python_callable=load,
        provide_context=True
    )

    t4 = PythonOperator(
        task_id="finish_success",
        python_callable=finish_success,
        provide_context=True
    )

    t1 >> t2 >> t3 >> t4