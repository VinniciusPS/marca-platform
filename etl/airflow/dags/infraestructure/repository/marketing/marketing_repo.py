import os
    from typing import List, Dict, Any
    
    from models.marketing import MarketingSearchTermModel, MarketingBenchmarkModel
    from infraestructure.database.postgres.postgres_handler import PostgresHandler
    
    
    class MarketingRepository:
        """Repositório para o schema marketing."""
    
        def __init__(self, handler: PostgresHandler):
            self.handler = handler
            self._queries_path = os.path.join(os.path.dirname(__file__), "queries")
    
        def _load_query(self, filename: str) -> str:
            path = os.path.join(self._queries_path, filename)
            with open(path, "r") as f:
                return f.read()
    
        def get_specialties(self) -> List[Dict[str, Any]]:
            query = self._load_query("select_specialties_for_marketing.sql")
            return self.handler.fetch_all(query)
    
        def upsert_search_terms(self, entities: List[MarketingSearchTermModel]) -> int:
            if not entities:
                return 0
            query = self._load_query("upsert_marketing_search_terms.sql")
            data = [e.model_dump() for e in entities]
            return self.handler.execute_upsert(query, data)
    
        def upsert_benchmarks(self, entities: List[MarketingBenchmarkModel]) -> int:
            if not entities:
                return 0
            query = self._load_query("upsert_marketing_benchmarks.sql")
            data = [e.model_dump() for e in entities]
            return self.handler.execute_upsert(query, data)