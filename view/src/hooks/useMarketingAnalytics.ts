import { useQuery } from "@tanstack/react-query";
import { marketingService } from "@/services/marketingService";
import type { MarketingAnalytics, MarketingFilters } from "@/types/marketing";

export function useMarketingAnalytics() {
  return useQuery({
    queryKey: ["marketing-analytics"],
    queryFn: () => marketingService.list(),
    staleTime: 60_000,
  });
}

export function applyFilters(
  data: MarketingAnalytics[],
  filters: MarketingFilters,
): MarketingAnalytics[] {
  return data.filter((row) => {
    if (
      filters.search &&
      !row.specialty.toLowerCase().includes(filters.search.toLowerCase())
    ) {
      return false;
    }
    if (
      filters.statuses?.length &&
      !filters.statuses.includes(row.mkt_strategy_status)
    ) {
      return false;
    }
    if (
      typeof filters.minMargin === "number" &&
      row.liquid_margin_after_cac < filters.minMargin
    ) {
      return false;
    }
    if (
      typeof filters.maxMargin === "number" &&
      row.liquid_margin_after_cac > filters.maxMargin
    ) {
      return false;
    }
    return true;
  });
}
