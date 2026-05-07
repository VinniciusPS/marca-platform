import { useMemo } from "react";
import { Activity, DollarSign, Target, TrendingUp } from "lucide-react";
import { KpiCard } from "./KpiCard";
import type { MarketingAnalytics } from "@/types/marketing";

const fmtBRL = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export function KpiSection({ data }: { data: MarketingAnalytics[] }) {
  const stats = useMemo(() => {
    if (!data.length) {
      return { specialties: 0, avgCpc: 0, avgCac: 0, avgMargin: 0 };
    }
    const sum = data.reduce(
      (acc, r) => ({
        cpc: acc.cpc + r.novo_cpc,
        cac: acc.cac + r.projected_cac,
        margin: acc.margin + r.liquid_margin_after_cac,
      }),
      { cpc: 0, cac: 0, margin: 0 },
    );
    const n = data.length;
    return {
      specialties: n,
      avgCpc: sum.cpc / n,
      avgCac: sum.cac / n,
      avgMargin: sum.margin / n,
    };
  }, [data]);

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <KpiCard
        label="Especialidades"
        value={String(stats.specialties)}
        hint="Total monitorado"
        icon={Activity}
        tone="primary"
      />
      <KpiCard
        label="CPC Médio"
        value={fmtBRL(stats.avgCpc)}
        hint="Custo por clique"
        icon={Target}
        tone="accent"
      />
      <KpiCard
        label="CAC Projetado"
        value={fmtBRL(stats.avgCac)}
        hint="Custo de aquisição"
        icon={DollarSign}
        tone="warning"
      />
      <KpiCard
        label="Margem Líquida"
        value={fmtBRL(stats.avgMargin)}
        hint="Após CAC"
        icon={TrendingUp}
        tone="success"
      />
    </div>
  );
}
