from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infraestructure.database import get_db
from infraestructure.persistence.repository import PatientRepository
from application.services.patient_service import PatientService
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])

# Injeção de Dependência Centralizada
def get_patient_service(db: AsyncSession = Depends(get_db)) -> PatientService:
    repository = PatientRepository(db)
    return PatientService(repository)

class PatientCreateSchema(BaseModel):
    name: str
    cpf: str

class PatientUpdateSchema(BaseModel):
    name: str

@router.post("/", status_code=201)
async def create(
    data: PatientCreateSchema, 
    service: PatientService = Depends(get_patient_service)
):
    return await service.register_patient(data.name, data.cpf)

@router.get("/")
async def list_all(service: PatientService = Depends(get_patient_service)):
    return await service.list_patients()

@router.put("/{id}")
async def update(
    id: int, 
    data: PatientUpdateSchema, 
    service: PatientService = Depends(get_patient_service)
):
    await service.update_patient_name(id, data.name)
    return {"status": "updated"}

@router.delete("/{id}")
async def delete(
    id: int, 
    service: PatientService = Depends(get_patient_service)
):
    success = await service.remove_patient(id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"status": "deleted"}