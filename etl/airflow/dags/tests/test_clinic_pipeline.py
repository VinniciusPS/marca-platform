import os
import unittest
from unittest.mock import MagicMock
from datetime import datetime

from pydantic import ValidationError

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
from infraestructure.repository.clinic.clinic_repo import ClinicRepository


class TestClinicModels(unittest.TestCase):
    """Testes unitários para validação dos DTOs do schema clinic."""

    def test_specialty_model_valid(self):
        spec = SpecialtyModel(name="Odontologia")
        dump = spec.model_dump()
        self.assertEqual(dump["name"], "Odontologia")

    def test_professional_model_valid_and_invalid(self):
        prof = ProfessionalModel(
            name="Dr. Silva",
            document_type="CRM",
            document_number="12345/SP-2023",
            specialty_id=1,
            is_active=True,
        )
        self.assertEqual(prof.document_type, "CRM")

        with self.assertRaises(ValidationError):
            ProfessionalModel(
                name="Dr. Silva",
                document_type="INVALID_TYPE",
                document_number="12345",
                specialty_id=1,
            )

    def test_professional_schedule_model_valid(self):
        sched = ProfessionalScheduleModel(
            professional_id=1,
            day_of_week=0,
            start_time="08:00:00",
            end_time="17:00:00",
        )
        self.assertEqual(sched.day_of_week, 0)

        with self.assertRaises(ValidationError):
            ProfessionalScheduleModel(
                professional_id=1,
                day_of_week=7,  # Inválido: deve ser 0-6
                start_time="08:00:00",
                end_time="17:00:00",
            )

    def test_appointment_model_status_validation(self):
        app = AppointmentModel(
            patient_id=1,
            professional_id=2,
            service_id=3,
            cid_id=4,
            appointment_date="2026-08-30",
            start_time="08:00:00",
            end_time="08:50:00",
            final_price="250.00",
            status="scheduled",
        )
        self.assertEqual(app.status, "scheduled")

        with self.assertRaises(ValidationError):
            AppointmentModel(
                patient_id=1,
                professional_id=2,
                service_id=3,
                cid_id=4,
                appointment_date="2026-08-30",
                start_time="08:00:00",
                end_time="08:50:00",
                status="invalid_status",
            )


class TestMockDataGenerator(unittest.TestCase):
    """Testes unitários para o gerador de dados mock agnóstico."""

    def setUp(self):
        self.factory = MockDataFactory(seed=42)

    def test_cpf_generation(self):
        cpf = self.factory._generate_cpf()
        self.assertEqual(len(cpf), 14)
        self.assertRegex(cpf, r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")

    def test_crm_generation(self):
        crm = self.factory._generate_crm()
        self.assertRegex(crm, r"^\d{5}/[A-Z]{2}-\d{4}$")

    def test_factory_generate_stream(self):
        config = {
            "name": {"type": "str", "pattern": "realistic"},
            "cpf": {"type": "str", "pattern": "cpf", "unique": True},
        }
        records = list(self.factory.generate(config, 10))
        self.assertEqual(len(records), 10)
        for r in records:
            self.assertIn("name", r)
            self.assertIn("cpf", r)


class TestClinicRepository(unittest.TestCase):
    """Testes unitários do repositório com mock do PostgresHandler."""

    def setUp(self):
        self.mock_handler = MagicMock()
        self.repo = ClinicRepository(handler=self.mock_handler)

    def test_upsert_specialties(self):
        self.mock_handler.execute_upsert.return_value = 2
        entities = [
            SpecialtyModel(name="Odontologia"),
            SpecialtyModel(name="Cardiologia"),
        ]
        result = self.repo.upsert_specialties(entities)
        self.assertEqual(result, 2)
        self.mock_handler.execute_upsert.assert_called_once()
        called_query = self.mock_handler.execute_upsert.call_args[0][0]
        self.assertIn(":name", called_query)
        self.assertIn("clinic.specialties", called_query)

    def test_get_specialty_ids(self):
        self.mock_handler.fetch_all.return_value = [
            {"specialty_id": 1},
            {"specialty_id": 2},
        ]
        ids = self.repo.get_specialty_ids()
        self.assertEqual(ids, [1, 2])

    def test_upsert_appointments(self):
        self.mock_handler.execute_upsert.return_value = 1
        entities = [
            AppointmentModel(
                patient_id=1,
                professional_id=1,
                service_id=1,
                cid_id=1,
                appointment_date="2026-08-30",
                start_time="09:00:00",
                end_time="09:50:00",
                final_price="300.00",
                status="completed",
            )
        ]
        result = self.repo.upsert_appointments(entities)
        self.assertEqual(result, 1)
        called_query = self.mock_handler.execute_upsert.call_args[0][0]
        self.assertIn(":patient_id", called_query)
        self.assertIn(":professional_id", called_query)


if __name__ == "__main__":
    unittest.main()
