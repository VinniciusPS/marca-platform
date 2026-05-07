export interface OperationsRow {
  professional_name: string;
  specialty: string;
  weekly_fixed_cost: number;
  be_threshold_units: number;
  service_price: number;
  variable_cost_per_service: number;
  actual_appointments: number;
  margin_per_appointment: number;
  weekly_net_profit: number;
  actionable_insight: string;
}

export interface OperationsFilters {
  search?: string;
  specialties?: string[];
  minProfit?: number;
  maxProfit?: number;
}
