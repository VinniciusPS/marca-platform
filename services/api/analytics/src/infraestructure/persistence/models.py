from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Integer, Numeric, Text
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

class CapacityAlertView(Base):
    """Mapeamento da View gld__capacity_alert no schema gold."""
    __tablename__ = "gld__capacity_alert"
    __table_args__ = {"schema": "silver"}

    # SQLAlchemy exige uma 'primary_key' para mapear, mesmo que seja uma View.
    # Usaremos o nome do profissional como identificador lógico.
    professional_name: Mapped[str] = mapped_column(Text, primary_key=True)
    specialty: Mapped[str] = mapped_column(String(50))
    weekly_fixed_cost: Mapped[float] = mapped_column(Numeric(10, 2))
    be_threshold_units: Mapped[int] = mapped_column(Integer)
    service_price: Mapped[float] = mapped_column(Numeric(10, 2))
    variable_cost_per_service: Mapped[float] = mapped_column(Numeric(10, 2))
    actual_appointments: Mapped[int] = mapped_column(Integer) # bigint mapeia para Integer no Python
    margin_per_appointment: Mapped[float] = mapped_column(Numeric)
    weekly_net_profit: Mapped[float] = mapped_column(Numeric)
    actionable_insight: Mapped[str] = mapped_column(Text)