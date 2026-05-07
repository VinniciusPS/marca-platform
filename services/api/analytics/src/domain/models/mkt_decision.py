from dataclasses import dataclass

@dataclass
class MktDecision:
    specialty: str
    scenario_delta: int
    novo_cpc: float
    projected_cac: float
    liquid_margin_after_cac: float
    mkt_strategy_status: str