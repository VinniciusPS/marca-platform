export type MktStrategyStatus =
  | "Agressividade Permitida"
  | "Manter Estratégia"
  | "Reduzir Investimento"
  | "Pausar Campanha";

export interface MarketingAnalytics {
  specialty: string;
  scenario_delta: number;
  novo_cpc: number;
  projected_cac: number;
  liquid_margin_after_cac: number;
  mkt_strategy_status: MktStrategyStatus | string;
}

export interface MarketingFilters {
  search?: string;
  statuses?: string[];
  minMargin?: number;
  maxMargin?: number;
}
