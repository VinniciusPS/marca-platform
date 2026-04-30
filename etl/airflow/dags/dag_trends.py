import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

from services.google_trends import GoogleTrendsService
from services.postgres import PostgresService
from services.load_control import LoadControlService
from repository.connection import get_engine

DATASET_NAME = "google_trends"

KEYWORD_GROUPS = {
    "odontologia": [
        "dor de dente",
        "dente inflamado",
        "siso inflamado"
    ]
}

def start_load(ti, **kwargs):
    print("START LOAD EXECUTING")

    engine = get_engine()
    svc = LoadControlService(engine)
    load_id = svc.start_load(DATASET_NAME)

    ti.xcom_push(key="load_id", value=load_id)

def extract(ti, **kwargs):
    engine = get_engine()
    load_svc = LoadControlService(engine)

    last_watermark = load_svc.get_last_successful_watermark(DATASET_NAME)

    timeframe = "now 2-d" if not last_watermark else "now 1-d"

    trends = GoogleTrendsService()
    df = trends.fetch(KEYWORD_GROUPS, timeframe)

    if df is None or df.empty:
        raise ValueError("No data returned from Google Trends")

    ti.xcom_push(key="dataframe", value=df.to_json())
    ti.xcom_push(key="rows_extracted", value=len(df))


def load(ti, **kwargs):
    engine = get_engine()
    pg = PostgresService(engine)

    df_json = ti.xcom_pull(key="dataframe")

    if not df_json:
        raise ValueError("No dataframe found in XCom")

    df = pd.read_json(df_json)

    pg.upsert_batch(df)

    ti.xcom_push(key="rows_loaded", value=len(df))

    last_date = df["date"].max() if not df.empty else None
    ti.xcom_push(key="last_extracted_at", value=str(last_date))


def finish_success(ti, **kwargs):
    engine = get_engine()
    svc = LoadControlService(engine)

    load_id = ti.xcom_pull(key="load_id")
    rows_extracted = ti.xcom_pull(key="rows_extracted")
    rows_loaded = ti.xcom_pull(key="rows_loaded")
    last_extracted_at = ti.xcom_pull(key="last_extracted_at")

    svc.finish_load(
        load_id=load_id,
        status="success",
        rows_extracted=rows_extracted,
        rows_loaded=rows_loaded,
        last_extracted_at=last_extracted_at
    )

def finish_failure(ti, **kwargs):
    engine = get_engine()
    svc = LoadControlService(engine)

    load_id = ti.xcom_pull(key="load_id")

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
    
    from airflow.utils.trigger_rule import TriggerRule

    t_fail = PythonOperator(
        task_id="finish_failure",
        python_callable=finish_failure,
        trigger_rule=TriggerRule.ONE_FAILED
    )

    t1 = PythonOperator(
        task_id="start_load",
        python_callable=start_load,
        
    )

    t2 = PythonOperator(
        task_id="extract",
        python_callable=extract,
        
    )

    t3 = PythonOperator(
        task_id="load",
        python_callable=load,
        
    )

    t4 = PythonOperator(
        task_id="finish_success",
        python_callable=finish_success,
        
    )

    t1 >> t2 >> t3 >> t4
    [t1, t2, t3] >> t_fail