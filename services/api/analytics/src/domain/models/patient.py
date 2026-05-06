from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Patient:
    name: str
    cpf: str
    patient_id: Optional[int] = None
    created_at: Optional[datetime] = None