from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import List, Optional
from domain.models.patient import Patient
from infraestructure.persistence.models import PatientTable

class PatientRepository:
    def __init__(self, session: AsyncSession):
        """Injeção de dependência da sessão assíncrona."""
        self.session = session

    async def insert(self, patient: Patient) -> Patient:
        db_patient = PatientTable(name=patient.name, cpf=patient.cpf)
        self.session.add(db_patient)
        await self.session.commit()
        await self.session.refresh(db_patient)
        
        # Mapeia de volta para a entidade de domínio pura
        return Patient(
            patient_id=db_patient.patient_id,
            name=db_patient.name,
            cpf=db_patient.cpf,
            created_at=db_patient.created_at
        )

    async def list_all(self) -> List[Patient]:
        result = await self.session.execute(select(PatientTable))
        rows = result.scalars().all()
        return [Patient(p.name, p.cpf, p.patient_id, p.created_at) for p in rows]

    async def find_by_id(self, p_id: int) -> Optional[Patient]:
        result = await self.session.get(PatientTable, p_id)
        if not result:
            return None
        return Patient(result.name, result.cpf, result.patient_id, result.created_at)

    async def update_patient(self, p_id: int, name: str) -> None:
        stmt = (
            update(PatientTable)
            .where(PatientTable.patient_id == p_id)
            .values(name=name)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def remove(self, p_id: int) -> bool:
        stmt = delete(PatientTable).where(PatientTable.patient_id == p_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0