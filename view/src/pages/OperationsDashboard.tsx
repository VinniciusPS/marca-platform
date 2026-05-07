import { useMemo, useState } from "react";
import { Activity } from "lucide-react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppShell } from "@/components/layout/AppShell";
import { OperationsKpiSection } from "@/components/operations/OperationsKpiSection";
import { OperationsTable } from "@/components/operations/OperationsTable";
import { OperationsFiltersSidebar } from "@/components/operations/OperationsFiltersSidebar";
import { applyOperationsFilters, useOperations } from "@/hooks/useOperations";
import type { OperationsFilters } from "@/types/operations";

export default function OperationsDashboard() {
  const { data = [], isLoading } = useOperations();
  const [filters, setFilters] = useState<OperationsFilters>({});

  const filtered = useMemo(() => applyOperationsFilters(data, filters), [data, filters]);
  const specialties = useMemo(
    () => Array.from(new Set(data.map((d) => d.specialty))).sort(),
    [data],
  );

  return (
    <AppShell>
      <SidebarProvider>
        <div className="flex flex-1 w-full min-w-0">
          <div className="flex-1 flex flex-col min-w-0">
            <header className="sticky top-0 z-10 flex h-14 items-center gap-3 border-b bg-card/80 px-4 backdrop-blur">
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
                  <Activity className="h-4 w-4" />
                </div>
                <div>
                  <h1 className="text-sm font-semibold leading-tight">Dashboard de Operações</h1>
                  <p className="text-xs text-muted-foreground leading-tight">
                    Análise de Break-Even por Profissional
                  </p>
                </div>
              </div>
              <SidebarTrigger className="ml-auto" />
            </header>

            <main className="flex-1 space-y-6 p-4 md:p-6">
              <OperationsKpiSection data={filtered} />
              <OperationsTable data={filtered} loading={isLoading} />
            </main>
          </div>

          <OperationsFiltersSidebar
            filters={filters}
            onChange={setFilters}
            specialties={specialties}
          />
        </div>
      </SidebarProvider>
    </AppShell>
  );
}
