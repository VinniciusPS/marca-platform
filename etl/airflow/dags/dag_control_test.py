# dags/test_infrastructure_control.py

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Apenas o necessário: O que salvar (Model) e onde salvar (Repo)
from infraestructure.database.postgres.connection import get_engine
from infraestructure.database.postgres.postgres_handler import PostgresHandler
from infraestructure.repository.control.control_repo import ControlRepository
from models.control import ETLLoadDTO, LoadStatus

def run_control_test():
    engine = get_engine()
    handler = PostgresHandler(engine=engine)
    # Instanciação direta e limpa sem vazamento de infraestrutura
    repo = ControlRepository(handler=handler)
    
    dataset_name = "test_clean_architecture_v1"
    
    # Início do ciclo de vida
    load_id = repo.create_initial_load(dataset_name)
    current_load = ETLLoadDTO(
        id=load_id, 
        dataset_name=dataset_name,
        status=LoadStatus.RUNNING
    )
    
    print(f"Carga iniciada com ID: {current_load.id}")

    try:
        # Simulação de lógica de sucesso
        current_load.status = LoadStatus.SUCCESS
        current_load.rows_extracted = 100
        current_load.rows_loaded = 100
        current_load.end_time = datetime.now()
        
        # Persistência final
        repo.update_load_status(current_load)
        print("Status atualizado para SUCCESS no banco.")

    except Exception as e:
        current_load.status = LoadStatus.FAILED
        current_load.error_message = str(e)
        current_load.end_time = datetime.now()
        repo.update_load_status(current_load)
        raise e

with DAG(
    dag_id="test_infrastructure_control_clean",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["clean_arch", "infra"],
) as dag:

    test_task = PythonOperator(
        task_id="test_control_logic",
        python_callable=run_control_test
    )

    test_task