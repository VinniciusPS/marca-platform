import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export function InsightBadge({ insight }: { insight: string }) {
  let cls = "bg-muted text-muted-foreground border-border";
  if (insight.includes("🚨") || insight.toUpperCase().includes("ABAIXO")) {
    cls = "bg-destructive/15 text-destructive border-destructive/30";
  } else if (insight.includes("⚠️")) {
    cls = "bg-warning/15 text-warning border-warning/30";
  } else if (insight.includes("✅") || insight.toUpperCase().includes("ACIMA")) {
    cls = "bg-success/15 text-success border-success/30";
  }
  return (
    <Badge variant="outline" className={cn("font-medium whitespace-nowrap", cls)}>
      {insight}
    </Badge>
  );
}
