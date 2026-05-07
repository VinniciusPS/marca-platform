import type { OperationsRow } from "@/types/operations";
import { apiFetch } from "./api";

const MOCK_DATA: OperationsRow[] = [
  {
    professional_name: "Dra. Ana Silva",
    specialty: "Nutrição",
    weekly_fixed_cost: 2400.0,
    be_threshold_units: 15,
    service_price: 180.0,
    variable_cost_per_service: 20.0,
    actual_appointments: 12,
    margin_per_appointment: 160,
    weekly_net_profit: -480,
    actionable_insight: "🚨 ABAIXO DO BE - Ociosidade Crítica",
  },
  {
    professional_name: "Dr. Bruno Costa",
    specialty: "Cardiologia",
    weekly_fixed_cost: 3200.0,
    be_threshold_units: 18,
    service_price: 250.0,
    variable_cost_per_service: 30.0,
    actual_appointments: 22,
    margin_per_appointment: 220,
    weekly_net_profit: 1640,
    actionable_insight: "✅ ACIMA DO BE - Capacidade Saudável",
  },
  {
    professional_name: "Dra. Carla Mendes",
    specialty: "Dermatologia",
    weekly_fixed_cost: 2800.0,
    be_threshold_units: 16,
    service_price: 220.0,
    variable_cost_per_service: 25.0,
    actual_appointments: 16,
    margin_per_appointment: 195,
    weekly_net_profit: 320,
    actionable_insight: "⚠️ NO BE - Monitorar Demanda",
  },
];

const USE_MOCK = (import.meta.env.VITE_USE_MOCK ?? "true") === "true";

export const operationsService = {
  async list(): Promise<OperationsRow[]> {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 200));
      return MOCK_DATA;
    }
    return apiFetch<OperationsRow[]>("/operations/analytics");
  },
};
