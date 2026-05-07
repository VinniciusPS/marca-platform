import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const STATUS_STYLES: Record<string, string> = {
  "Agressividade Permitida": "bg-success/15 text-success border-success/30",
  "Manter Estratégia": "bg-primary/15 text-primary border-primary/30",
  "Reduzir Investimento": "bg-warning/15 text-warning border-warning/30",
  "Pausar Campanha": "bg-destructive/15 text-destructive border-destructive/30",
};

export function StrategyStatusBadge({ status }: { status: string }) {
  const cls = STATUS_STYLES[status] ?? "bg-muted text-muted-foreground border-border";
  return (
    <Badge variant="outline" className={cn("font-medium", cls)}>
      {status}
    </Badge>
  );
}
