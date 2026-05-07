from dataclasses import dataclass

@dataclass
class CapacityAlert:
    professional_name: str
    specialty: str
    weekly_fixed_cost: float
    be_threshold_units: int
    service_price: float
    variable_cost_per_service: float
    actual_appointments: int
    margin_per_appointment: float
    weekly_net_profit: float
    actionable_insight: str