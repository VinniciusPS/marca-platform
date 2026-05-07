import { Search } from "lucide-react";
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
import type { MarketingFilters } from "@/types/marketing";

const STATUS_OPTIONS = [
  "Agressividade Permitida",
  "Manter Estratégia",
  "Reduzir Investimento",
  "Pausar Campanha",
];

interface FiltersSidebarProps {
  filters: MarketingFilters;
  onChange: (filters: MarketingFilters) => void;
}

export function FiltersSidebar({ filters, onChange }: FiltersSidebarProps) {
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
        <p className="text-xs text-muted-foreground">Refine os resultados</p>
      </SidebarHeader>
      <SidebarContent className="px-3 py-4">
        <SidebarGroup>
          <SidebarGroupLabel>Buscar</SidebarGroupLabel>
          <SidebarGroupContent>
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                value={filters.search ?? ""}
                onChange={(e) => onChange({ ...filters, search: e.target.value })}
                placeholder="Especialidade..."
                className="pl-8"
              />
            </div>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Estratégia</SidebarGroupLabel>
          <SidebarGroupContent className="space-y-2 px-2 pt-1">
            {STATUS_OPTIONS.map((status) => {
              const id = `status-${status}`;
              const checked = filters.statuses?.includes(status) ?? false;
              return (
                <div key={status} className="flex items-center gap-2">
                  <Checkbox
                    id={id}
                    checked={checked}
                    onCheckedChange={() => toggleStatus(status)}
                  />
                  <Label htmlFor={id} className="text-sm font-normal cursor-pointer">
                    {status}
                  </Label>
                </div>
              );
            })}
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Margem após CAC (R$)</SidebarGroupLabel>
          <SidebarGroupContent className="space-y-2 px-2 pt-1">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label htmlFor="min-margin" className="text-xs text-muted-foreground">Mín</Label>
                <Input
                  id="min-margin"
                  type="number"
                  value={filters.minMargin ?? ""}
                  onChange={(e) =>
                    onChange({
                      ...filters,
                      minMargin: e.target.value === "" ? undefined : Number(e.target.value),
                    })
                  }
                />
              </div>
              <div>
                <Label htmlFor="max-margin" className="text-xs text-muted-foreground">Máx</Label>
                <Input
                  id="max-margin"
                  type="number"
                  value={filters.maxMargin ?? ""}
                  onChange={(e) =>
                    onChange({
                      ...filters,
                      maxMargin: e.target.value === "" ? undefined : Number(e.target.value),
                    })
                  }
                />
              </div>
            </div>
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
