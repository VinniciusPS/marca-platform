from typing import Any, List

from infraestructure.database.base_handler import DataHandler
from sqlalchemy import text

class PostgresHandler(DataHandler):
    def __init__(self, engine, batch_size: int = 500):
        self.engine = engine
        self._batch_size = batch_size

    @property
    def batch_size(self) -> int:
        return self._batch_size

    def execute_scalar(self, query: str, params: dict = None) -> Any:
        """Executa query e retorna o primeiro valor da primeira linha (ex: ID)."""
        with self.engine.begin() as conn:
            result = conn.execute(text(query), params or {})
            return result.scalar()

    def execute(self, query: str, params: dict = None) -> None:
        """Executa um comando (UPDATE/INSERT) sem retorno."""
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    def execute_upsert(self, query: str, data: List[dict]) -> int:
        if not data:
            return 0
        with self.engine.begin() as conn:
            conn.execute(text(query), data)
        return len(data)