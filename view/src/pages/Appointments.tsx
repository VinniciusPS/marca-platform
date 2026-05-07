import { useMemo, useState } from "react";
import { CalendarCheck } from "lucide-react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppShell } from "@/components/layout/AppShell";
import { AppointmentsFiltersSidebar } from "@/components/appointments/AppointmentsFiltersSidebar";
import { AppointmentsTable } from "@/components/appointments/AppointmentsTable";
import { NewAppointmentDialog } from "@/components/appointments/NewAppointmentDialog";
import {
  applyAppointmentFilters,
  useAppointments,
} from "@/hooks/useAppointments";
import type { AppointmentFilters } from "@/types/appointments";

export default function Appointments() {
  const { data = [], isLoading } = useAppointments();
  const [filters, setFilters] = useState<AppointmentFilters>({});
  const [dialogOpen, setDialogOpen] = useState(false);

  const filtered = useMemo(
    () => applyAppointmentFilters(data, filters),
    [data, filters],
  );

  return (
    <AppShell>
      <SidebarProvider>
        <div className="flex flex-1 w-full min-w-0">
          <div className="flex-1 flex flex-col min-w-0">
            <header className="sticky top-0 z-10 flex h-14 items-center gap-3 border-b bg-card/80 px-4 backdrop-blur">
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
                  <CalendarCheck className="h-4 w-4" />
                </div>
                <div>
                  <h1 className="text-sm font-semibold leading-tight">
                    Appointments
                  </h1>
                  <p className="text-xs text-muted-foreground leading-tight">
                    Gerenciamento de agendamentos
                  </p>
                </div>
              </div>
              <SidebarTrigger className="ml-auto" />
            </header>

            <main className="flex-1 space-y-6 p-4 md:p-6">
              <AppointmentsTable
                data={filtered}
                loading={isLoading}
                onNewAppointment={() => setDialogOpen(true)}
              />
            </main>
          </div>

          <AppointmentsFiltersSidebar filters={filters} onChange={setFilters} />
        </div>
      </SidebarProvider>

      <NewAppointmentDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
      />
    </AppShell>
  );
}
