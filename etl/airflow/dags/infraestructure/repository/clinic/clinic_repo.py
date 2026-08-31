import os
from typing import List, Dict, Any

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
from infraestructure.database.postgres.postgres_handler import PostgresHandler


class ClinicRepository:
    """
    Repositório de persistência e leitura para o schema clinic.
    """

    def __init__(self, handler: PostgresHandler):
        self.handler = handler
        self._queries_path = os.path.join(os.path.dirname(__file__), "queries")

    def _load_query(self, filename: str) -> str:
        path = os.path.join(self._queries_path, filename)
        with open(path, "r") as f:
            return f.read()

    # --- Specialties ---
    def upsert_specialties(self, entities: List[SpecialtyModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_specialties.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    def get_specialty_ids(self) -> List[int]:
        rows = self.handler.fetch_all("SELECT specialty_id FROM clinic.specialties ORDER BY specialty_id ASC;")
        return [r["specialty_id"] for r in rows]

    # --- Professionals ---
    def upsert_professionals(self, entities: List[ProfessionalModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_professionals.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    def get_professional_ids(self) -> List[int]:
        rows = self.handler.fetch_all("SELECT professional_id FROM clinic.professionals ORDER BY professional_id ASC;")
        return [r["professional_id"] for r in rows]

    # --- Professional Schedules ---
    def upsert_professional_schedules(self, entities: List[ProfessionalScheduleModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_professional_schedules.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    # --- Schedule Exceptions ---
    def upsert_schedule_exceptions(self, entities: List[ScheduleExceptionModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_schedule_exceptions.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    # --- Patients ---
    def upsert_patients(self, entities: List[PatientModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_patients.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    def get_patient_ids(self) -> List[int]:
        rows = self.handler.fetch_all("SELECT patient_id FROM clinic.patients ORDER BY patient_id ASC;")
        return [r["patient_id"] for r in rows]

    # --- CID Codes ---
    def upsert_cid_codes(self, entities: List[CIDCodeModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_cid_codes.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    def get_cid_ids(self) -> List[int]:
        rows = self.handler.fetch_all("SELECT cid_id FROM clinic.cid_codes ORDER BY cid_id ASC;")
        return [r["cid_id"] for r in rows]

    # --- Services ---
    def upsert_services(self, entities: List[ServiceModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_services.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)

    def get_services(self) -> List[Dict[str, Any]]:
        return self.handler.fetch_all("SELECT service_id, specialty_id, base_price FROM clinic.services ORDER BY service_id ASC;")

    # --- Appointments ---
    def upsert_appointments(self, entities: List[AppointmentModel]) -> int:
        if not entities:
            return 0
        query = self._load_query("upsert_appointments.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)
