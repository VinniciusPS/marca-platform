import os
from typing import List, Dict, Any

from models.operations import ProfessionalContractModel
from infraestructure.database.postgres.postgres_handler import PostgresHandler


class OperationsRepository:
    """
    Repositório de persistência e consulta para o schema operations.
    """

    def __init__(self, handler: PostgresHandler):
        self.handler = handler
        self._queries_path = os.path.join(os.path.dirname(__file__), "queries")

    def _load_query(self, filename: str) -> str:
        path = os.path.join(self._queries_path, filename)
        with open(path, "r") as f:
            return f.read()

    def get_professionals_with_specialty(self) -> List[Dict[str, Any]]:
        """Consulta profissionais e especialidades de clinic a partir de arquivo SQL."""
        query = self._load_query("select_active_professionals_specialties.sql")
        return self.handler.fetch_all(query)

    def upsert_contracts(self, entities: List[ProfessionalContractModel]) -> int:
        """Executa o upsert em lote na tabela operations.professional_contracts."""
        if not entities:
            return 0
        query = self._load_query("upsert_professional_contracts.sql")
        data = [e.model_dump() for e in entities]
        return self.handler.execute_upsert(query, data)
