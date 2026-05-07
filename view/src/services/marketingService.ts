import type { MarketingAnalytics } from "@/types/marketing";
import { apiFetch } from "./api";

/**
 * Mocked data — to be replaced by FastAPI endpoint:
 *   GET /marketing/analytics
 */
const MOCK_DATA: MarketingAnalytics[] = [
  {
    specialty: "Nutrição",
    scenario_delta: 0,
    novo_cpc: 5.5,
    projected_cac: 55,
    liquid_margin_after_cac: 25,
    mkt_strategy_status: "Agressividade Permitida",
  },
];

const USE_MOCK = (import.meta.env.VITE_USE_MOCK ?? "true") === "true";

export const marketingService = {
  async list(): Promise<MarketingAnalytics[]> {
    if (USE_MOCK) {
      // Simulate latency for realistic UX testing.
      await new Promise((r) => setTimeout(r, 200));
      return MOCK_DATA;
    }
    return apiFetch<MarketingAnalytics[]>("/marketing/analytics");
  },
};
