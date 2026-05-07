import type { MarketingAnalytics } from "@/types/marketing";
import { apiFetch } from "./api";

const API_BASE_URL = import.meta.env.VITE_API_URL;

// Mantemos o mock apenas como fallback de segurança, mas a lógica agora prioriza a API
const MOCK_DATA: MarketingAnalytics[] = [
  {
    specialty: "Nutrição (Mock)",
    scenario_delta: 0,
    novo_cpc: 5.5,
    projected_cac: 55,
    liquid_margin_after_cac: 25,
    mkt_strategy_status: "Agressividade Permitida",
  },
];

// Corrigido: Se VITE_USE_MOCK for "true", usa o mock. Caso contrário, vai para a API.
const SHOULD_USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";

export const marketingService = {
  async list(): Promise<MarketingAnalytics[]> {
    if (SHOULD_USE_MOCK) {
      await new Promise((r) => setTimeout(r, 200));
      return MOCK_DATA;
    }

    return apiFetch<MarketingAnalytics[]>("/analytics/mkt-decisions");
  },
};

