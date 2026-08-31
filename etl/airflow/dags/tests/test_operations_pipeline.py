import unittest
from unittest.mock import MagicMock
from decimal import Decimal

from pydantic import ValidationError

from models.operations import ProfessionalContractModel
from infraestructure.repository.operations.operations_repo import OperationsRepository


class TestOperationsModels(unittest.TestCase):
    """Testes unitários para o DTO de contratos profissionais."""

    def test_valid_contract_model(self):
        contract = ProfessionalContractModel(
            professional_id=1,
            specialty="Cardiologia",
            weekly_hours_contracted=40,
            weekly_fixed_cost="3500.00",
            service_price="300.00",
            variable_cost_per_service="50.00",
            be_threshold_units=14,
        )
        dump = contract.model_dump()
        self.assertEqual(dump["professional_id"], 1)
        self.assertEqual(dump["be_threshold_units"], 14)

    def test_create_factory_method_calculation(self):
        # fixed = 3000, price = 250, var = 50 -> margin = 200 -> be_units = 3000/200 = 15
        contract = ProfessionalContractModel.create(
            professional_id=2,
            specialty="Odontologia",
            weekly_hours=30,
            fixed_cost=Decimal("3000.00"),
            price=Decimal("250.00"),
            variable_cost=Decimal("50.00"),
        )
        self.assertEqual(contract.be_threshold_units, 15)
        self.assertEqual(contract.weekly_fixed_cost, "3000.00")

    def test_create_factory_method_margin_protection(self):
        # price <= var_cost deve ser ajustado para garantir margem positiva
        contract = ProfessionalContractModel.create(
            professional_id=3,
            specialty="Dermatologia",
            weekly_hours=20,
            fixed_cost=Decimal("2000.00"),
            price=Decimal("50.00"),
            variable_cost=Decimal("60.00"),
        )
        self.assertGreater(contract.be_threshold_units, 0)

    def test_invalid_contract_model(self):
        with self.assertRaises(ValidationError):
            ProfessionalContractModel(
                professional_id=-1,
                specialty="Cardiologia",
                weekly_hours_contracted=200,
                weekly_fixed_cost="3000.00",
                service_price="200.00",
                variable_cost_per_service="30.00",
                be_threshold_units=-5,
            )


class TestOperationsRepository(unittest.TestCase):
    """Testes unitários para o repositório de operations."""

    def setUp(self):
        self.mock_handler = MagicMock()
        self.repo = OperationsRepository(handler=self.mock_handler)

    def test_get_professionals_with_specialty(self):
        self.mock_handler.fetch_all.return_value = [
            {"professional_id": 1, "specialty": "Odontologia"},
            {"professional_id": 2, "specialty": "Cardiologia"},
        ]
        profs = self.repo.get_professionals_with_specialty()
        self.assertEqual(len(profs), 2)
        self.assertEqual(profs[0]["specialty"], "Odontologia")
        self.mock_handler.fetch_all.assert_called_once()
        called_query = self.mock_handler.fetch_all.call_args[0][0]
        self.assertIn("clinic.professionals", called_query)

    def test_upsert_contracts(self):
        self.mock_handler.execute_upsert.return_value = 1
        entities = [
            ProfessionalContractModel(
                professional_id=1,
                specialty="Dermatologia",
                weekly_hours_contracted=30,
                weekly_fixed_cost="2800.00",
                service_price="250.00",
                variable_cost_per_service="40.00",
                be_threshold_units=14,
            )
        ]
        result = self.repo.upsert_contracts(entities)
        self.assertEqual(result, 1)
        called_query = self.mock_handler.execute_upsert.call_args[0][0]
        self.assertIn("operations.professional_contracts", called_query)
        self.assertIn(":be_threshold_units", called_query)


if __name__ == "__main__":
    unittest.main()
