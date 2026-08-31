"""
Domain models para o schema clinic.
Contrato entre layers: Mock/Mapper → Repository → Database
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, time
from typing import Optional
from decimal import Decimal


class SpecialtyModel(BaseModel):
    """
    Model para especialidades médicas.
    Contrato: entre Mock/Mapper e Repository.
    """
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., min_length=1)
    created_at: Optional[datetime] = None


class ProfessionalModel(BaseModel):
    """
    Model para profissionais (médicos, dentistas, etc).
    """
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., min_length=1)
    document_type: str = Field(..., pattern="^(CRM|CPF)$")
    document_number: str = Field(..., min_length=1)
    specialty_id: int = Field(..., gt=0)
    is_active: bool = True
    created_at: Optional[datetime] = None


class ProfessionalScheduleModel(BaseModel):
    """
    Model para horários de disponibilidade semanal.
    day_of_week: 0=segunda, 6=domingo
    """
    model_config = ConfigDict(from_attributes=True)
    
    professional_id: int = Field(..., gt=0)
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: str = Field(...)  # HH:MM:SS formato
    end_time: str = Field(...)    # HH:MM:SS formato
    created_at: Optional[datetime] = None


class ScheduleExceptionModel(BaseModel):
    """
    Model para exceções de agenda (férias, feriados, ausências).
    """
    model_config = ConfigDict(from_attributes=True)
    
    professional_id: int = Field(..., gt=0)
    start_datetime: datetime
    end_datetime: datetime
    reason: Optional[str] = None
    created_at: Optional[datetime] = None


class PatientModel(BaseModel):
    """
    Model para pacientes.
    CPF é opcional e único quando presente.
    """
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., min_length=1)
    cpf: Optional[str] = None
    created_at: Optional[datetime] = None


class CIDCodeModel(BaseModel):
    """
    Model para códigos CID (Classificação Internacional de Doenças).
    """
    model_config = ConfigDict(from_attributes=True)
    
    code: str = Field(..., min_length=1)
    description: Optional[str] = None


class ServiceModel(BaseModel):
    """
    Model para serviços oferecidos.
    Cada serviço pertence a uma especialidade.
    """
    model_config = ConfigDict(from_attributes=True)
    
    specialty_id: int = Field(..., gt=0)
    service_name: str = Field(..., min_length=1)
    base_price: str = Field(...)  # Decimal como string para XCom
    created_at: Optional[datetime] = None


class AppointmentModel(BaseModel):
    """
    Model para agendamentos (consultas/procedimentos).
    """
    model_config = ConfigDict(from_attributes=True)
    
    patient_id: int = Field(..., gt=0)
    professional_id: int = Field(..., gt=0)
    service_id: int = Field(..., gt=0)
    cid_id: int = Field(..., gt=0)
    appointment_date: str = Field(...)  # YYYY-MM-DD
    start_time: str = Field(...)  # HH:MM:SS
    end_time: str = Field(...)    # HH:MM:SS
    final_price: Optional[str] = None  # Decimal como string
    status: str = Field(
        default="scheduled",
        pattern="^(scheduled|completed|cancelled|no_show|inquiry)$"
    )
    created_at: Optional[datetime] = None
