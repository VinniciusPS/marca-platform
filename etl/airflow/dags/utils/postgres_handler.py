from sqlalchemy import text
from itertools import islice

class PostgresHandler:
    def __init__(self, engine, batch_size: int = 500):
        self.engine = engine
        self.batch_size = batch_size

    def execute_upsert(self, query: str, data: list) -> int:
        """
        Executa um batch bruto. Não mexe no dado, apenas obedece.
        """
        if not data:
            return 0
            
        with self.engine.begin() as conn:
            conn.execute(text(query), data)
        return len(data)