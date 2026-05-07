import { useQuery } from "@tanstack/react-query";
import { operationsService } from "@/services/operationsService";
import type { OperationsRow, OperationsFilters } from "@/types/operations";

export function useOperations() {
  return useQuery({
    queryKey: ["operations-analytics"],
    queryFn: () => operationsService.list(),
    staleTime: 60_000,
  });
}

export function applyOperationsFilters(
  data: OperationsRow[],
  filters: OperationsFilters,
): OperationsRow[] {
  return data.filter((row) => {
    if (
      filters.search &&
      !row.professional_name.toLowerCase().includes(filters.search.toLowerCase())
    ) {
      return false;
    }
    if (
      filters.specialties?.length &&
      !filters.specialties.includes(row.specialty)
    ) {
      return false;
    }
    if (
      typeof filters.minProfit === "number" &&
      row.weekly_net_profit < filters.minProfit
    ) {
      return false;
    }
    if (
      typeof filters.maxProfit === "number" &&
      row.weekly_net_profit > filters.maxProfit
    ) {
      return false;
    }
    return true;
  });
}
