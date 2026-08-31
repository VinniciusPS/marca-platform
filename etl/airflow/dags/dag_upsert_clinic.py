from datetime import datetime
from typing import List, Dict, Any

from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule

from models.control import ETLLoadDTO, LoadStatus
from models.clinic import (
    SpecialtyModel,
    ProfessionalModel,
    ProfessionalScheduleModel,
    ScheduleExceptionModel,
    PatientModel,
    CIDCodeModel,
    ServiceModel,
    AppointmentModel,
)
from utils.mock_data_generator import MockDataFactory
from infraestructure.database.postgres.connection import get_engine
from infraestructure.database.postgres.postgres_handler import PostgresHandler
from infraestructure.repository.control.control_repo import ControlRepository
from infraestructure.repository.clinic.clinic_repo import ClinicRepository


@dag(
    dag_id="pipeline_upsert_clinic_data",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["clinic", "mock_data", "upsert"],
)
def clinic_upsert_pipeline():
    """
    Pipeline de população e atualização do schema clinic com dados mock gerados via MockDataFactory.
    Garante integridade referencial executando cargas em ordem topológica:
    1. Especialidades, Pacientes e CIDs
    2. Profissionais e Serviços
    3. Agendas e Exceções
    4. Agendamentos
    """

    def get_control_repo() -> ControlRepository:
        return ControlRepository(handler=PostgresHandler(engine=get_engine()))

    def get_clinic_repo() -> ClinicRepository:
        return ClinicRepository(handler=PostgresHandler(engine=get_engine()))

    @task
    def start_pipeline() -> dict:
        repo = get_control_repo()
        dataset_name = "clinic_data"
        load_id = repo.create_initial_load(dataset_name)
        return {"load_id": load_id, "dataset_name": dataset_name}

    # --- Estágio 1: Entidades Independentes ---

    @task
    def load_specialties(rows_quantity: int = 10) -> int:
        repo = get_clinic_repo()
        factory = MockDataFactory()
        config = {
            "name": {
                "type": "str",
                "pattern": "choice",
                "choices": [
                    "Odontologia", "Cardiologia", "Dermatologia", "Ortopedia",
                    "Pediatria", "Ginecologia", "Neurologia", "Oftalmologia",
                    "Psiquiatria", "Endocrinologia", "Fisioterapia", "Nutrição",
                ],
                "unique": True,
            }
        }
        entities = [
            SpecialtyModel(**record)
            for record in factory.generate(config, min(rows_quantity, 12))
        ]
        return repo.upsert_specialties(entities)

    @task
    def load_patients(rows_quantity: int = 50) -> int:
        repo = get_clinic_repo()
        factory = MockDataFactory()
        config = {
            "name": {"type": "str", "pattern": "realistic"},
            "cpf": {"type": "str", "pattern": "cpf", "unique": True},
        }
        entities = [
            PatientModel(**record)
            for record in factory.generate(config, rows_quantity)
        ]
        return repo.upsert_patients(entities)

    @task
    def load_cid_codes(rows_quantity: int = 15) -> int:
        repo = get_clinic_repo()
        factory = MockDataFactory()
        config = {
            "code": {
                "type": "str",
                "pattern": "choice",
                "choices": [
                    "K02.1", "K05.0", "I10", "E11", "J00",
                    "M54.5", "L20", "H52.1", "F41.1", "E66",
                    "K21.0", "M79.1", "Z00.0", "Z01.2", "R51",
                ],
                "unique": True,
            },
            "description": {
                "type": "str",
                "pattern": "choice",
                "choices": [
                    "Cárie da dentina", "Gengivite aguda", "Hipertensão essencial",
                    "Diabetes mellitus", "Nasofaringite aguda", "Dor lombar baixa",
                    "Dermatite atópica", "Miopia", "Ansiedade generalizada",
                    "Obesidade", "Doença do refluxo", "Mialgia",
                    "Exame médico geral", "Exame odontológico", "Cefaleia",
                ],
            },
        }
        entities = [
            CIDCodeModel(**record)
            for record in factory.generate(config, min(rows_quantity, 15))
        ]
        return repo.upsert_cid_codes(entities)

    # --- Estágio 2: Entidades Dependentes de Especialidades ---

    @task
    def load_professionals(specialties_synced: int, rows_quantity: int = 20) -> int:
        repo = get_clinic_repo()
        specialty_ids = repo.get_specialty_ids()
        if not specialty_ids:
            return 0

        factory = MockDataFactory()
        config = {
            "name": {"type": "str", "pattern": "realistic"},
            "document_type": {"type": "str", "pattern": "choice", "choices": ["CRM", "CPF"]},
            "document_number": {"type": "str", "pattern": "crm", "unique": True},
            "specialty_id": {"type": "int", "choice": specialty_ids},
            "is_active": {"type": "bool", "true_probability": 0.95},
        }
        entities = []
        for record in factory.generate(config, rows_quantity):
            record["name"] = f"Dr(a). {record['name']}"
            if record["document_type"] == "CPF":
                record["document_number"] = factory._generate_cpf()
            entities.append(ProfessionalModel(**record))

        return repo.upsert_professionals(entities)

    @task
    def load_services(specialties_synced: int, rows_quantity: int = 25) -> int:
        repo = get_clinic_repo()
        specialty_ids = repo.get_specialty_ids()
        if not specialty_ids:
            return 0

        factory = MockDataFactory()
        config = {
            "specialty_id": {"type": "int", "choice": specialty_ids},
            "service_name": {
                "type": "str",
                "pattern": "choice",
                "choices": [
                    "Consulta Especializada", "Consulta de Retorno", "Avaliação Inicial",
                    "Procedimento Diagnóstico", "Tratamento Terapêutico", "Exame Clínico",
                    "Limpeza e Profilaxia", "Exame Preventivo", "Consulta de Urgência",
                    "Sessão de Acompanhamento",
                ],
            },
            "base_price": {"type": "decimal", "range": [120.0, 650.0]},
        }
        entities = [
            ServiceModel(**record)
            for record in factory.generate(config, rows_quantity)
        ]
        return repo.upsert_services(entities)

    # --- Estágio 3: Agendas e Exceções (Dependentes de Profissionais) ---

    @task
    def load_professional_schedules(professionals_synced: int) -> int:
        repo = get_clinic_repo()
        prof_ids = repo.get_professional_ids()
        if not prof_ids:
            return 0

        entities = []
        for prof_id in prof_ids:
            for day in range(5):  # Segunda a sexta
                entities.append(
                    ProfessionalScheduleModel(
                        professional_id=prof_id,
                        day_of_week=day,
                        start_time="08:00:00",
                        end_time="17:00:00",
                    )
                )
        return repo.upsert_professional_schedules(entities)

    @task
    def load_schedule_exceptions(professionals_synced: int, rows_quantity: int = 15) -> int:
        repo = get_clinic_repo()
        prof_ids = repo.get_professional_ids()
        if not prof_ids:
            return 0

        factory = MockDataFactory()
        config = {
            "professional_id": {"type": "int", "choice": prof_ids},
            "start_datetime": {"type": "datetime", "days_offset": -20},
            "end_datetime": {"type": "datetime", "days_offset": 20},
            "reason": {
                "type": "str",
                "pattern": "choice",
                "choices": [
                    "Férias programadas",
                    "Participação em Congresso Médico",
                    "Licença médica",
                    "Feriado institucional",
                    "Treinamento de capacitação",
                ],
            },
        }
        entities = []
        for record in factory.generate(config, rows_quantity):
            start_dt = datetime.fromisoformat(record["start_datetime"]) if isinstance(record["start_datetime"], str) else record["start_datetime"]
            end_dt = datetime.fromisoformat(record["end_datetime"]) if isinstance(record["end_datetime"], str) else record["end_datetime"]
            if start_dt > end_dt:
                start_dt, end_dt = end_dt, start_dt
            entities.append(
                ScheduleExceptionModel(
                    professional_id=record["professional_id"],
                    start_datetime=start_dt,
                    end_datetime=end_dt,
                    reason=record["reason"],
                )
            )
        return repo.upsert_schedule_exceptions(entities)

    # --- Estágio 4: Agendamentos ---

    @task
    def load_appointments(
        schedules_synced: int,
        exceptions_synced: int,
        services_synced: int,
        patients_synced: int,
        cid_synced: int,
        rows_quantity: int = 100,
    ) -> int:
        repo = get_clinic_repo()
        patient_ids = repo.get_patient_ids()
        prof_ids = repo.get_professional_ids()
        services = repo.get_services()
        cid_ids = repo.get_cid_ids()

        if not (patient_ids and prof_ids and services and cid_ids):
            return 0

        service_ids = [s["service_id"] for s in services]
        factory = MockDataFactory()
        config = {
            "patient_id": {"type": "int", "choice": patient_ids},
            "professional_id": {"type": "int", "choice": prof_ids},
            "service_id": {"type": "int", "choice": service_ids},
            "cid_id": {"type": "int", "choice": cid_ids},
            "appointment_date": {"type": "date", "days_offset": -15},
            "start_time": {
                "type": "str",
                "pattern": "choice",
                "choices": ["08:00:00", "09:00:00", "10:00:00", "11:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00"],
            },
            "end_time": {
                "type": "str",
                "pattern": "choice",
                "choices": ["08:50:00", "09:50:00", "10:50:00", "11:50:00", "13:50:00", "14:50:00", "15:50:00", "16:50:00", "17:50:00"],
            },
            "final_price": {"type": "decimal", "range": [150.0, 750.0]},
            "status": {
                "type": "str",
                "pattern": "choice",
                "choices": ["scheduled", "completed", "cancelled", "no_show", "inquiry"],
            },
        }
        entities = [
            AppointmentModel(**record)
            for record in factory.generate(config, rows_quantity)
        ]
        return repo.upsert_appointments(entities)

    # --- Finalização ---

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def finalize_pipeline(load_context: dict, total_appointments: int):
        repo = get_control_repo()
        load_dto = ETLLoadDTO(
            id=load_context["load_id"],
            dataset_name=load_context["dataset_name"],
            status=LoadStatus.SUCCESS,
            rows_extracted=total_appointments,
            rows_loaded=total_appointments,
            end_time=datetime.now(),
        )
        repo.update_load_status(load_dto)

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def handle_failure(load_context: dict, **context):
        repo = get_control_repo()
        ti = context.get("ti")
        error_msg = f"Falha na task: {ti.task_id}" if ti else "Falha desconhecida no pipeline clinic"
        load_dto = ETLLoadDTO(
            id=load_context["load_id"],
            dataset_name=load_context["dataset_name"],
            status=LoadStatus.FAILED,
            error_message=error_msg,
            end_time=datetime.now(),
        )
        repo.update_load_status(load_dto)
        raise Exception(error_msg)

    # --- Orquestração e Topologia ---
    load_ctx = start_pipeline()

    # Nível 1
    spec_count = load_specialties()
    pat_count = load_patients()
    cid_count = load_cid_codes()

    # Nível 2
    prof_count = load_professionals(spec_count)
    svc_count = load_services(spec_count)

    # Nível 3
    sched_count = load_professional_schedules(prof_count)
    exc_count = load_schedule_exceptions(prof_count)

    # Nível 4
    app_count = load_appointments(
        sched_count, exc_count, svc_count, pat_count, cid_count
    )

    # Finalização
    finalize_pipeline(load_ctx, app_count)
    [spec_count, pat_count, cid_count, prof_count, svc_count, sched_count, exc_count, app_count] >> handle_failure(load_ctx)


clinic_pipeline_dag = clinic_upsert_pipeline()
