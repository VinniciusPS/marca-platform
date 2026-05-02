from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# DTO de Entrada: Reflete o dado bruto que o Extrator retira da fonte (PyTrends)
class GoogleTrendsRawDTO(BaseModel):
    """
    Representa o registro individual após o processamento inicial do Extrator.
    Este é o contrato entre o Extrator e o Mapper.
    """
    date: datetime
    keyword: str
    value: int
    group_name: str

# DTO de Saída: Reflete o contrato final que será persistido no Postgres
class GoogleTrendsStorageDTO(BaseModel):
    """
    Representa o registro pronto para o Loader. 
    """
    model_config = ConfigDict(from_attributes=True)
    
    source_date: datetime
    keyword: str
    group_name: str
    specialty: str
    interest: int
    created_at: datetime
    updated_at: datetime