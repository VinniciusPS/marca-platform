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
import type { OperationsFilters } from "@/types/operations";

interface Props {
  filters: OperationsFilters;
  onChange: (f: OperationsFilters) => void;
  specialties: string[];
}

export function OperationsFiltersSidebar({ filters, onChange, specialties }: Props) {
  const toggleSpecialty = (s: string) => {
    const cur = filters.specialties ?? [];
    onChange({
      ...filters,
      specialties: cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s],
    });
  };

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
                placeholder="Profissional..."
                className="pl-8"
              />
            </div>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Especialidade</SidebarGroupLabel>
          <SidebarGroupContent className="space-y-2 px-2 pt-1">
            {specialties.map((s) => {
              const id = `spec-${s}`;
              const checked = filters.specialties?.includes(s) ?? false;
              return (
                <div key={s} className="flex items-center gap-2">
                  <Checkbox id={id} checked={checked} onCheckedChange={() => toggleSpecialty(s)} />
                  <Label htmlFor={id} className="text-sm font-normal cursor-pointer">
                    {s}
                  </Label>
                </div>
              );
            })}
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Lucro Líquido (R$)</SidebarGroupLabel>
          <SidebarGroupContent className="space-y-2 px-2 pt-1">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label htmlFor="min-profit" className="text-xs text-muted-foreground">Mín</Label>
                <Input
                  id="min-profit"
                  type="number"
                  value={filters.minProfit ?? ""}
                  onChange={(e) =>
                    onChange({
                      ...filters,
                      minProfit: e.target.value === "" ? undefined : Number(e.target.value),
                    })
                  }
                />
              </div>
              <div>
                <Label htmlFor="max-profit" className="text-xs text-muted-foreground">Máx</Label>
                <Input
                  id="max-profit"
                  type="number"
                  value={filters.maxProfit ?? ""}
                  onChange={(e) =>
                    onChange({
                      ...filters,
                      maxProfit: e.target.value === "" ? undefined : Number(e.target.value),
                    })
                  }
                />
              </div>
            </div>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupContent className="px-2">
            <Button variant="outline" size="sm" className="w-full" onClick={() => onChange({})}>
              Limpar filtros
            </Button>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
