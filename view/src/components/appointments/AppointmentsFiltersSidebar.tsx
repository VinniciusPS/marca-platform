import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
} from "@/components/ui/sidebar";
import type { AppointmentFilters } from "@/types/appointments";
import {
  APPOINTMENT_STATUSES,
  APPOINTMENT_STATUS_LABELS,
} from "./AppointmentStatusBadge";

interface AppointmentsFiltersSidebarProps {
  filters: AppointmentFilters;
  onChange: (filters: AppointmentFilters) => void;
}

export function AppointmentsFiltersSidebar({
  filters,
  onChange,
}: AppointmentsFiltersSidebarProps) {
  const toggleStatus = (status: string) => {
    const current = filters.statuses ?? [];
    onChange({
      ...filters,
      statuses: current.includes(status)
        ? current.filter((s) => s !== status)
        : [...current, status],
    });
  };

  const reset = () => onChange({});

  return (
    <Sidebar collapsible="icon" side="right">
      <SidebarHeader className="border-b px-4 py-4">
        <h2 className="text-sm font-semibold tracking-tight">Filtros</h2>
        <p className="text-xs text-muted-foreground">Refine os agendamentos</p>
      </SidebarHeader>
      <SidebarContent className="px-3 py-4">
        <SidebarGroup>
          <SidebarGroupLabel>Buscar por data</SidebarGroupLabel>
          <SidebarGroupContent className="px-2 pt-1">
            <Input
              type="date"
              value={filters.date ?? ""}
              onChange={(e) =>
                onChange({
                  ...filters,
                  date: e.target.value === "" ? undefined : e.target.value,
                })
              }
            />
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Status</SidebarGroupLabel>
          <SidebarGroupContent className="space-y-2 px-2 pt-1">
            {APPOINTMENT_STATUSES.map((status) => {
              const id = `appt-status-${status}`;
              const checked = filters.statuses?.includes(status) ?? false;
              return (
                <div key={status} className="flex items-center gap-2">
                  <Checkbox
                    id={id}
                    checked={checked}
                    onCheckedChange={() => toggleStatus(status)}
                  />
                  <Label
                    htmlFor={id}
                    className="text-sm font-normal cursor-pointer"
                  >
                    {APPOINTMENT_STATUS_LABELS[status] ?? status}
                  </Label>
                </div>
              );
            })}
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupContent className="px-2">
            <Button variant="outline" size="sm" className="w-full" onClick={reset}>
              Limpar filtros
            </Button>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
