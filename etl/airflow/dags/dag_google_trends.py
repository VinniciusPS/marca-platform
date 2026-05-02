import os
from datetime import datetime, timezone
from typing import List

from models.control import ETLLoadDTO, LoadStatus
from models.google_trends import GoogleTrendsRawDTO, GoogleTrendsStorageDTO
from infraestructure.database.postgres.connection import get_engine
from infraestructure.database.postgres.postgres_handler import PostgresHandler
from infraestructure.repository.control.control_repo import ControlRepository
from infraestructure.repository.google_trends.google_trends_repo import GoogleTrendsRepository
from services.google_trends.extractor import GoogleTrendsExtractor
from services.google_trends.mapper import GoogleTrendsMapper

from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule

@dag(
    dag_id="pipeline_google_trends_real",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["google_trends", "real_data"],
)
def google_trends_pipeline():

    def get_control_repo():
        return ControlRepository(handler=PostgresHandler(engine=get_engine()))

    @task
    def start_pipeline():
        repo = get_control_repo()
        dataset_name = "google_trends"
        load_id = repo.create_initial_load(dataset_name)
        return {"load_id": load_id, "dataset_name": dataset_name}

    @task
    def extract_trends():
        """Responsabilidade Única: Extração e Mapeamento para Raw."""
        extractor = GoogleTrendsExtractor()
        
        keyword_groups = {"saude_odontologia": ["dentista", "aparelho ortodôntico"]}
        timeframe = "today 1-m"
        
        # Extrai e converte para lista de dicts (para serialização XCom)
        raw_stream = extractor.fetch_stream(keyword_groups, timeframe)
        return [raw.model_dump(mode="json") for raw in raw_stream]

    @task
    def load_trends(raw_data: list):
        """Responsabilidade Única: Transformação de Domínio e Persistência."""
        if not raw_data:
            return 0
            
        handler = PostgresHandler(engine=get_engine())
        mapper = GoogleTrendsMapper()
        repo = GoogleTrendsRepository(handler=handler)

        # Reconstrói os DTOs a partir do XCom
        raw_dtos = (GoogleTrendsRawDTO(**d) for d in raw_data)
        
        # Transforma (Raw -> Storage) e persiste
        storage_entities = list(mapper.transform_stream(raw_dtos))
        return repo.upsert_batch(storage_entities)

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def finalize_pipeline(load_context: dict, rows_count: int):
        repo = get_control_repo()
        load_dto = ETLLoadDTO(
            id=load_context['load_id'],
            dataset_name=load_context['dataset_name'],
            status=LoadStatus.SUCCESS,
            rows_extracted=rows_count,
            rows_loaded=rows_count,
            end_time=datetime.now()
        )
        repo.update_load_status(load_dto)

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def handle_failure(load_context: dict, **context):
        repo = get_control_repo()
        ti = context['ti']
        error_msg = f"Falha na task: {ti.task_id}"
        
        load_dto = ETLLoadDTO(
            id=load_context['load_id'],
            dataset_name=load_context['dataset_name'],
            status=LoadStatus.FAILED,
            error_message=error_msg,
            end_time=datetime.now()
        )
        repo.update_load_status(load_dto)
        raise Exception(error_msg)

    # --- Fluxo de Dependências ---
    load_ctx = start_pipeline()
    
    raw_list = extract_trends()
    rows_affected = load_trends(raw_list)
    
    # Orquestração de finalização
    rows_affected >> finalize_pipeline(load_ctx, rows_affected)
    
    # Qualquer falha no meio do caminho dispara o erro
    [raw_list, rows_affected] >> handle_failure(load_ctx)

google_trends_pipeline()