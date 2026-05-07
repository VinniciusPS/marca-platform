from abc import ABC, abstractmethod
from typing import List, Any

class DataHandler(ABC):
    @property
    @abstractmethod
    def batch_size(self) -> int:
        pass

    @abstractmethod
    def execute_upsert(self, query: str, data: List[dict]) -> int:
        pass