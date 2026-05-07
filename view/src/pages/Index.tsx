import { useMemo, useState } from "react";
import { HeartPulse } from "lucide-react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppShell } from "@/components/layout/AppShell";
import { FiltersSidebar } from "@/components/dashboard/FiltersSidebar";
import { KpiSection } from "@/components/dashboard/KpiSection";
import { AnalyticsTable } from "@/components/dashboard/AnalyticsTable";
import { MarginBarChart } from "@/components/dashboard/MarginBarChart";
import { applyFilters, useMarketingAnalytics } from "@/hooks/useMarketingAnalytics";
import type { MarketingFilters } from "@/types/marketing";

const Index = () => {
  const { data = [], isLoading } = useMarketingAnalytics();
  const [filters, setFilters] = useState<MarketingFilters>({});

  const filtered = useMemo(() => applyFilters(data, filters), [data, filters]);

  return (
    <AppShell>
      <SidebarProvider>
        <div className="flex flex-1 w-full min-w-0">
          <div className="flex-1 flex flex-col min-w-0">
            <header className="sticky top-0 z-10 flex h-14 items-center gap-3 border-b bg-card/80 px-4 backdrop-blur">
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
                  <HeartPulse className="h-4 w-4" />
                </div>
                <div>
                  <h1 className="text-sm font-semibold leading-tight">Dashboard de Gestão</h1>
                  <p className="text-xs text-muted-foreground leading-tight">
                    Marketing Analytics por Especialidade
                  </p>
                </div>
              </div>
              <SidebarTrigger className="ml-auto" />
            </header>

            <main className="flex-1 space-y-6 p-4 md:p-6">
              <KpiSection data={filtered} />
              <MarginBarChart data={filtered} />
              <AnalyticsTable data={filtered} loading={isLoading} />
            </main>
          </div>

          <FiltersSidebar filters={filters} onChange={setFilters} />
        </div>
      </SidebarProvider>
    </AppShell>
  );
};

export default Index;
