import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { AppointmentStatusBadge } from "./AppointmentStatusBadge";
import type { Appointment } from "@/types/appointments";

const fmtBRL = (v: number | null) =>
  v === null
    ? "—"
    : v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const fmtDate = (iso: string) => {
  const [y, m, d] = iso.split("-");
  return `${d}/${m}/${y}`;
};

const fmtTime = (t: string) => t.slice(0, 5);

interface AppointmentsTableProps {
  data: Appointment[];
  loading?: boolean;
  onNewAppointment: () => void;
}

export function AppointmentsTable({
  data,
  loading,
  onNewAppointment,
}: AppointmentsTableProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0">
        <CardTitle className="text-lg">Agendamentos</CardTitle>
        <Button size="sm" onClick={onNewAppointment}>
          <Plus className="h-4 w-4" />
          Novo agendamento
        </Button>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow className="border-b-2 border-border hover:bg-transparent">
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">#</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Paciente</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Profissional</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Serviço</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">CID</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Data</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Horário</TableHead>
                <TableHead className="h-10 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">Valor</TableHead>
                <TableHead className="h-10 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={9} className="text-center text-muted-foreground py-8">
                    Carregando...
                  </TableCell>
                </TableRow>
              ) : data.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={9} className="text-center text-muted-foreground py-8">
                    Nenhum agendamento encontrado.
                  </TableCell>
                </TableRow>
              ) : (
                data.map((row) => (
                  <TableRow key={row.appointment_id}>
                    <TableCell className="font-medium tabular-nums">{row.appointment_id}</TableCell>
                    <TableCell className="tabular-nums">{row.patient_id}</TableCell>
                    <TableCell className="tabular-nums">{row.professional_id}</TableCell>
                    <TableCell className="tabular-nums">{row.service_id}</TableCell>
                    <TableCell className="tabular-nums">{row.cid_id}</TableCell>
                    <TableCell className="tabular-nums">{fmtDate(row.appointment_date)}</TableCell>
                    <TableCell className="tabular-nums">
                      {fmtTime(row.start_time)} – {fmtTime(row.end_time)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums font-medium">
                      {fmtBRL(row.final_price)}
                    </TableCell>
                    <TableCell>
                      <AppointmentStatusBadge status={row.status} />
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
