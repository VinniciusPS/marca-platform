import os
from models.control import ETLLoadDTO, LoadStatus
from infraestructure.database.postgres.postgres_handler import PostgresHandler

class ControlRepository:
    def __init__(self, handler: PostgresHandler):
        self.handler = handler
        self._queries_path = os.path.join(os.path.dirname(__file__), "queries")

    def _load_query(self, filename: str) -> str:
        path = os.path.join(self._queries_path, filename)
        with open(path, "r") as f:
            return f.read()

    def create_initial_load(self, dataset_name: str) -> int:
        """Cria o registro 'running' e retorna o ID gerado."""
        query = self._load_query("start_load.sql")
        # Retorna o ID para que a DAG possa controlar esse ciclo de vida
        return self.handler.execute_scalar(query, {"name": dataset_name})

    def update_load_status(self, load_data: ETLLoadDTO):
        """
        Recebe a model completa e atualiza o banco.
        O uso do model_dump() garante que todos os campos batam com o SQL.
        """
        query = self._load_query("update_load.sql")
        
        # Converte a model (incluindo Enums e Datetimes) para formato que o driver entende
        params = load_data.model_dump()
        
        self.handler.execute(query, params)