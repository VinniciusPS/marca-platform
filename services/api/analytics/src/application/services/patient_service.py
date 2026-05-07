from typing import List, Optional
from domain.models.patient import Patient
from infraestructure.persistence.repository import PatientRepository

class PatientService:
    def __init__(self, repository: PatientRepository):
        """O serviço não sabe o que é uma Session, ele apenas usa o repositório."""
        self.repository = repository

    async def register_patient(self, name: str, cpf: str) -> Patient:
        patient = Patient(name=name, cpf=cpf)
        return await self.repository.insert(patient)

    async def list_patients(self) -> List[Patient]:
        return await self.repository.list_all()

    async def get_patient_detail(self, p_id: int) -> Optional[Patient]:
        return await self.repository.find_by_id(p_id)

    async def update_patient_name(self, p_id: int, name: str) -> None:
        await self.repository.update_patient(p_id, name)

    async def remove_patient(self, p_id: int) -> bool:
        return await self.repository.remove(p_id)