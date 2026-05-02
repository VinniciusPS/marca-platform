from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

class LoadStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class ETLLoadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    dataset_name: str
    status: LoadStatus = LoadStatus.RUNNING
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    last_extracted_at: Optional[datetime] = None
    rows_extracted: int = 0
    rows_loaded: int = 0
    error_message: Optional[str] = None