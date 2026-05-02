# infrastructure/repository/google_trends/google_trends_repository.py

import os
from typing import List
from models.google_trends import GoogleTrendsStorageDTO
from infraestructure.database.postgres.postgres_handler import PostgresHandler

class GoogleTrendsRepository:
    def __init__(self, handler: PostgresHandler):
        self.handler = handler
        # Definimos o caminho da query relativo ao arquivo do repositório
        self._query_path = os.path.join(
            os.path.dirname(__file__), 
            "queries/upsert.sql"
        )

    def _get_query(self) -> str:
        with open(self._query_path, "r") as f:
            return f.read()

    def upsert_batch(self, trends_entities: List[GoogleTrendsStorageDTO]) -> int:
        """
        Recebe uma lista de entidades (DTOs), converte para dicionários 
        e orquestra o upsert via Handler.
        """
        if not trends_entities:
            return 0

        query = self._get_query()
        
        # Converte a lista de objetos Pydantic para lista de dicts
        # O Pydantic cuida da serialização de datas e enums automaticamente
        data = [entity.model_dump() for entity in trends_entities]
        
        return self.handler.execute_upsert(query, data)