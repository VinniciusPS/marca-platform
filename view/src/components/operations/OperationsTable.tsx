import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { InsightBadge } from "./InsightBadge";
import { cn } from "@/lib/utils";
import type { OperationsRow } from "@/types/operations";

const fmtBRL = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const headCls =
  "h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground";

export function OperationsTable({
  data,
  loading,
}: {
  data: OperationsRow[];
  loading?: boolean;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">
          Análise Operacional por Profissional
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow className="border-b-2 border-border hover:bg-transparent">
                <TableHead className={headCls}>Profissional</TableHead>
                <TableHead className={headCls}>Especialidade</TableHead>
                <TableHead className={cn(headCls, "text-right")}>Custo Fixo Sem.</TableHead>
                <TableHead className={cn(headCls, "text-right")}>BE (un)</TableHead>
                <TableHead className={cn(headCls, "text-right")}>Preço</TableHead>
                <TableHead className={cn(headCls, "text-right")}>Custo Variável</TableHead>
                <TableHead className={cn(headCls, "text-right")}>Atendim. Reais</TableHead>
                <TableHead className={cn(headCls, "text-right")}>Margem / Atend.</TableHead>
                <TableHead className={cn(headCls, "text-right")}>Lucro Líq. Sem.</TableHead>
                <TableHead className={headCls}>Insight</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={10} className="text-center text-muted-foreground py-8">
                    Carregando...
                  </TableCell>
                </TableRow>
              ) : data.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={10} className="text-center text-muted-foreground py-8">
                    Nenhum resultado encontrado.
                  </TableCell>
                </TableRow>
              ) : (
                data.map((row) => (
                  <TableRow key={row.professional_name}>
                    <TableCell className="font-medium">{row.professional_name}</TableCell>
                    <TableCell>{row.specialty}</TableCell>
                    <TableCell className="text-right tabular-nums">{fmtBRL(row.weekly_fixed_cost)}</TableCell>
                    <TableCell className="text-right tabular-nums">{row.be_threshold_units}</TableCell>
                    <TableCell className="text-right tabular-nums">{fmtBRL(row.service_price)}</TableCell>
                    <TableCell className="text-right tabular-nums">{fmtBRL(row.variable_cost_per_service)}</TableCell>
                    <TableCell className="text-right tabular-nums">{row.actual_appointments}</TableCell>
                    <TableCell className="text-right tabular-nums">{fmtBRL(row.margin_per_appointment)}</TableCell>
                    <TableCell
                      className={cn(
                        "text-right tabular-nums font-medium",
                        row.weekly_net_profit < 0 ? "text-destructive" : "text-success",
                      )}
                    >
                      {fmtBRL(row.weekly_net_profit)}
                    </TableCell>
                    <TableCell>
                      <InsightBadge insight={row.actionable_insight} />
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
