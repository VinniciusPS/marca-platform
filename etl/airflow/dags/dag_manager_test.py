import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from managers.google_trends_manager import GoogleTrendsManager
from services.google_trends.extractor import GoogleTrendsExtractor
from services.google_trends.mapper import GoogleTrendsMapper
from utils.postgres_handler import PostgresHandler
from repository.connection import get_engine

# Configurações de Teste
TEST_KEYWORD_GROUPS = {
    "teste_manager_odonto": ["aparelho invisivel", "implante dentario"]
}

def load_sql_file():
    """Lógica de carregamento do SQL para evitar paths fixos no Manager"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(current_dir, "repository/queries/google_trends/upsert.sql")
    with open(sql_path, "r") as f:
        return f.read()

def run_manager_integration_test():
    print("--- INICIANDO TESTE INTEGRADO DO MANAGER ---")
    
    # 1. Setup de Infraestrutura
    engine = get_engine()
    sql_query = load_sql_file()
    
    # 2. Injeção de Dependências (Clean Code)
    manager = GoogleTrendsManager(
        extractor=GoogleTrendsExtractor(),
        mapper=GoogleTrendsMapper(),
        handler=PostgresHandler(engine, batch_size=50) # Batch menor para teste
    )
    
    # 3. Execução do Fluxo
    # Usaremos um timeframe curto (últimas 48h) para não sobrecarregar
    total = manager.run(
        query=sql_query,
        keyword_groups=TEST_KEYWORD_GROUPS,
        timeframe="now 7-d"
    )
    
    print(f"--- TESTE FINALIZADO ---")
    print(f"Registros processados e persistidos no banco: {total}")
    
    return {"total_inserted": total}

with DAG(
    dag_id="test_google_trends_manager",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["integration", "manager", "db"]
) as dag:

    t_test_manager = PythonOperator(
        task_id="run_full_pipeline_test",
        python_callable=run_manager_integration_test
    )

    t_test_manager