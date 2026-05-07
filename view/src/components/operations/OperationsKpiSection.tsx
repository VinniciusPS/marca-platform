import { useMemo } from "react";
import { DollarSign, TrendingUp, Users } from "lucide-react";
import { KpiCard } from "@/components/dashboard/KpiCard";
import type { OperationsRow } from "@/types/operations";

const fmtBRL = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export function OperationsKpiSection({ data }: { data: OperationsRow[] }) {
  const stats = useMemo(() => {
    if (!data.length) return { profs: 0, totalProfit: 0, avgOccupancy: 0 };
    const totalProfit = data.reduce((a, r) => a + r.weekly_net_profit, 0);
    const avgOccupancy =
      data.reduce(
        (a, r) =>
          a +
          (r.be_threshold_units > 0
            ? (r.actual_appointments / r.be_threshold_units) * 100
            : 0),
        0,
      ) / data.length;
    return { profs: data.length, totalProfit, avgOccupancy };
  }, [data]);

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <KpiCard
        label="Profissionais"
        value={String(stats.profs)}
        hint="Total monitorado"
        icon={Users}
        tone="primary"
      />
      <KpiCard
        label="Lucro Líquido Semanal"
        value={fmtBRL(stats.totalProfit)}
        hint="Soma da carteira"
        icon={DollarSign}
        tone={stats.totalProfit >= 0 ? "success" : "warning"}
      />
      <KpiCard
        label="Ocupação Média"
        value={`${stats.avgOccupancy.toLocaleString("pt-BR", { maximumFractionDigits: 1 })}%`}
        hint="vs. Break-Even"
        icon={TrendingUp}
        tone="accent"
      />
    </div>
  );
}
