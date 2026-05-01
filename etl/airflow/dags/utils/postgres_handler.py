from typing import List

from utils.base_handler import DataHandler
from sqlalchemy import text

class PostgresHandler(DataHandler):
    def __init__(self, engine, batch_size: int = 500):
        self.engine = engine
        self._batch_size = batch_size

    @property
    def batch_size(self) -> int:
        return self._batch_size

    def execute_upsert(self, query: str, data: List[dict]) -> int:
        if not data:
            return 0
        with self.engine.begin() as conn:
            conn.execute(text(query), data)
        return len(data)