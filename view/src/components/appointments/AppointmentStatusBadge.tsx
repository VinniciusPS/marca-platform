import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const STATUS_STYLES: Record<string, string> = {
  scheduled: "bg-primary/15 text-primary border-primary/30",
  completed: "bg-success/15 text-success border-success/30",
  cancelled: "bg-destructive/15 text-destructive border-destructive/30",
  no_show: "bg-warning/15 text-warning border-warning/30",
};

const STATUS_LABELS: Record<string, string> = {
  scheduled: "Agendado",
  completed: "Concluído",
  cancelled: "Cancelado",
  no_show: "Não compareceu",
};

export function AppointmentStatusBadge({ status }: { status: string }) {
  const cls =
    STATUS_STYLES[status] ?? "bg-muted text-muted-foreground border-border";
  return (
    <Badge variant="outline" className={cn("font-medium", cls)}>
      {STATUS_LABELS[status] ?? status}
    </Badge>
  );
}

export const APPOINTMENT_STATUSES = Object.keys(STATUS_STYLES);
export { STATUS_LABELS as APPOINTMENT_STATUS_LABELS };
