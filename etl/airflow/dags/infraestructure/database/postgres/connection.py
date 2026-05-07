from airflow.providers.postgres.hooks.postgres import PostgresHook

def get_engine(conn_id="render_postgres"):
    hook = PostgresHook(postgres_conn_id=conn_id)
    return hook.get_sqlalchemy_engine()