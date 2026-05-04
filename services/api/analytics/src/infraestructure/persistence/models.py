from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
    pass

class PatientTable(Base):
    __tablename__ = "patients"
    __table_args__ = {"schema": "clinic"}

    patient_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())