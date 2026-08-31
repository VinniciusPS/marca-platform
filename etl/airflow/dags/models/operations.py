"""
Domain models para o schema operations.
Contrato entre layers: Mock/Mapper → Repository → Database
"""

import math
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class ProfessionalContractModel(BaseModel):
    """
    Model para contratos operacionais e detalhes econômicos de profissionais.
    """
    model_config = ConfigDict(from_attributes=True)

    professional_id: int = Field(..., gt=0)
    specialty: str = Field(..., min_length=1)
    weekly_hours_contracted: int = Field(..., ge=1, le=168)
    weekly_fixed_cost: str = Field(...)
    service_price: str = Field(...)
    variable_cost_per_service: str = Field(...)
    be_threshold_units: int = Field(..., ge=0)

    @classmethod
    def create(
        cls,
        professional_id: int,
        specialty: str,
        weekly_hours: int,
        fixed_cost: Decimal,
        price: Decimal,
        variable_cost: Decimal,
    ) -> "ProfessionalContractModel":
        """Factory method que valida margem e calcula o break-even de forma determinística."""
        # Garantir margem de contribuição unitária estritamente positiva
        if price <= variable_cost:
            price = variable_cost + Decimal("100.00")

        margin = price - variable_cost
        be_units = int(math.ceil(float(fixed_cost / margin))) if margin > Decimal("0.00") else 1

        return cls(
            professional_id=professional_id,
            specialty=specialty,
            weekly_hours_contracted=weekly_hours,
            weekly_fixed_cost=f"{fixed_cost:.2f}",
            service_price=f"{price:.2f}",
            variable_cost_per_service=f"{variable_cost:.2f}",
            be_threshold_units=be_units,
        )
