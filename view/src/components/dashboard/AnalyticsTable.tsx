import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StrategyStatusBadge } from "./StrategyStatusBadge";
import type { MarketingAnalytics } from "@/types/marketing";

const fmtBRL = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const fmtDelta = (v: number) =>
  `${v > 0 ? "+" : ""}${v.toLocaleString("pt-BR")}`;

export function AnalyticsTable({
  data,
  loading,
}: {
  data: MarketingAnalytics[];
  loading?: boolean;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Analytics de Marketing por Especialidade</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow className="border-b-2 border-border hover:bg-transparent">
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Especialidade</TableHead>
                <TableHead className="h-10 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">Δ Cenário</TableHead>
                <TableHead className="h-10 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">Novo CPC</TableHead>
                <TableHead className="h-10 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">CAC Projetado</TableHead>
                <TableHead className="h-10 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">Margem após CAC</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Estratégia</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                    Carregando...
                  </TableCell>
                </TableRow>
              ) : data.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                    Nenhum resultado encontrado.
                  </TableCell>
                </TableRow>
              ) : (
                data.map((row) => (
                  <TableRow key={row.specialty}>
                    <TableCell className="font-medium">{row.specialty}</TableCell>
                    <TableCell className="text-right tabular-nums">
                      {fmtDelta(row.scenario_delta)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {fmtBRL(row.novo_cpc)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {fmtBRL(row.projected_cac)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums font-medium">
                      {fmtBRL(row.liquid_margin_after_cac)}
                    </TableCell>
                    <TableCell>
                      <StrategyStatusBadge status={row.mkt_strategy_status} />
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
