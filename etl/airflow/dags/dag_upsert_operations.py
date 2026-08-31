from datetime import datetime
from decimal import Decimal

from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule

from models.control import ETLLoadDTO, LoadStatus
from models.operations import ProfessionalContractModel
from utils.mock_data_generator import MockDataFactory
from infraestructure.database.postgres.connection import get_engine
from infraestructure.database.postgres.postgres_handler import PostgresHandler
from infraestructure.repository.control.control_repo import ControlRepository
from infraestructure.repository.operations.operations_repo import OperationsRepository


@dag(
    dag_id="pipeline_upsert_operations_data",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["operations", "mock_data", "upsert", "capacity_alert"],
)
def operations_upsert_pipeline():
    """
    Pipeline de carga de contratos operacionais (operations.professional_contracts).
    Garante que os contratos reflitam os profissionais e especialidades reais do clinic,
    calculando com precisão o break-even (be_threshold_units) para os modelos dbt de capacity_alert.
    """

    def get_control_repo() -> ControlRepository:
        return ControlRepository(handler=PostgresHandler(engine=get_engine()))

    def get_operations_repo() -> OperationsRepository:
        return OperationsRepository(handler=PostgresHandler(engine=get_engine()))

    @task
    def start_pipeline() -> dict:
        repo = get_control_repo()
        dataset_name = "operations_data"
        load_id = repo.create_initial_load(dataset_name)
        return {"load_id": load_id, "dataset_name": dataset_name}

    @task
    def load_professional_contracts() -> int:
        repo = get_operations_repo()
        professionals = repo.get_professionals_with_specialty()
        if not professionals:
            return 0

        factory = MockDataFactory()
        config = {
            "weekly_hours_contracted": {"type": "int", "choice": [20, 24, 30, 36, 40]},
            "weekly_fixed_cost": {"type": "decimal", "range": [2000.0, 5500.0]},
            "service_price": {"type": "decimal", "range": [180.0, 450.0]},
            "variable_cost_per_service": {"type": "decimal", "range": [25.0, 70.0]},
        }

        mock_stream = factory.generate(config, len(professionals))
        entities = [
            ProfessionalContractModel.create(
                professional_id=prof["professional_id"],
                specialty=prof["specialty"],
                weekly_hours=mock_data["weekly_hours_contracted"],
                fixed_cost=Decimal(mock_data["weekly_fixed_cost"]),
                price=Decimal(mock_data["service_price"]),
                variable_cost=Decimal(mock_data["variable_cost_per_service"]),
            )
            for prof, mock_data in zip(professionals, mock_stream)
        ]

        return repo.upsert_contracts(entities)

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def finalize_pipeline(load_context: dict, total_contracts: int):
        repo = get_control_repo()
        load_dto = ETLLoadDTO(
            id=load_context["load_id"],
            dataset_name=load_context["dataset_name"],
            status=LoadStatus.SUCCESS,
            rows_extracted=total_contracts,
            rows_loaded=total_contracts,
            end_time=datetime.now(),
        )
        repo.update_load_status(load_dto)

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def handle_failure(load_context: dict, **context):
        repo = get_control_repo()
        ti = context.get("ti")
        error_msg = f"Falha na task: {ti.task_id}" if ti else "Falha desconhecida no pipeline operations"
        load_dto = ETLLoadDTO(
            id=load_context["load_id"],
            dataset_name=load_context["dataset_name"],
            status=LoadStatus.FAILED,
            error_message=error_msg,
            end_time=datetime.now(),
        )
        repo.update_load_status(load_dto)
        raise Exception(error_msg)

    # Orquestração
    load_ctx = start_pipeline()
    contracts_count = load_professional_contracts()

    finalize_pipeline(load_ctx, contracts_count)
    contracts_count >> handle_failure(load_ctx)


operations_pipeline_dag = operations_upsert_pipeline()
