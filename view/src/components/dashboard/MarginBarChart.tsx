import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { MarketingAnalytics } from "@/types/marketing";

const fmtPct = (v: number) =>
  `${v.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

export function MarginBarChart({ data }: { data: MarketingAnalytics[] }) {
  const rows = data.map((d) => {
    const total = d.projected_cac + d.liquid_margin_after_cac;
    const pct = total > 0 ? (d.liquid_margin_after_cac / total) * 100 : 0;
    return { specialty: d.specialty, pct };
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Margem Líquida — % sobre (CAC + Margem)</CardTitle>
      </CardHeader>
      <CardContent>
        {rows.length === 0 ? (
          <p className="text-sm text-muted-foreground py-6 text-center">
            Sem dados para exibir.
          </p>
        ) : (
          <ul className="space-y-4">
            {rows.map((r) => (
              <li key={r.specialty} className="grid grid-cols-[140px_1fr_64px] items-center gap-3">
                <span className="text-sm font-medium truncate">{r.specialty}</span>
                <div
                  className="relative h-3 w-full overflow-hidden rounded-full bg-muted"
                  role="progressbar"
                  aria-valuenow={Math.round(r.pct)}
                  aria-valuemin={0}
                  aria-valuemax={100}
                >
                  <div
                    className="h-full rounded-full bg-success transition-all"
                    style={{ width: `${Math.min(100, Math.max(0, r.pct))}%` }}
                  />
                </div>
                <span className="text-sm tabular-nums text-right text-muted-foreground">
                  {fmtPct(r.pct)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
