import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  BarChart3,
  CalendarCheck,
  ChevronLeft,
  ChevronRight,
  HeartPulse,
  LayoutDashboard,
  Settings2,
  Stethoscope,
  Users,
  Activity,
} from "lucide-react";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

const MODULES = [
  { to: "/appointments", label: "Appointments", icon: CalendarCheck },
  { to: "/patients", label: "Patients", icon: Users },
  { to: "/professionals", label: "Professionals", icon: Stethoscope },
  { to: "/operations", label: "Operations", icon: Settings2 },
];

const DASHBOARDS = [
  { to: "/", label: "Marketing", icon: BarChart3 },
  { to: "/dashboard/operations", label: "Operations", icon: Activity },
];

const itemBase =
  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors";

export function ModuleSideNav() {
  const { pathname } = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const dashboardActive =
    pathname === "/" || pathname.startsWith("/dashboard");

  const renderItem = (
    to: string,
    label: string,
    Icon: typeof CalendarCheck,
  ) => {
    const link = (
      <NavLink
        key={to}
        to={to}
        className={({ isActive }) =>
          cn(
            itemBase,
            collapsed && "justify-center px-0",
            isActive
              ? "bg-primary/10 text-primary"
              : "text-muted-foreground hover:bg-muted hover:text-foreground",
          )
        }
      >
        <Icon className="h-4 w-4 shrink-0" />
        {!collapsed && <span>{label}</span>}
      </NavLink>
    );

    if (!collapsed) return link;
    return (
      <Tooltip key={to}>
        <TooltipTrigger asChild>{link}</TooltipTrigger>
        <TooltipContent side="right">{label}</TooltipContent>
      </Tooltip>
    );
  };

  return (
    <TooltipProvider delayDuration={100}>
      <aside
        className={cn(
          "sticky top-0 z-20 flex h-screen shrink-0 flex-col border-r bg-card transition-[width] duration-200",
          collapsed ? "w-14" : "w-56",
        )}
      >
        <div
          className={cn(
            "flex h-14 items-center border-b",
            collapsed ? "justify-center px-2" : "gap-2 px-4",
          )}
        >
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
            <HeartPulse className="h-4 w-4" />
          </div>
          {!collapsed && (
            <span className="text-sm font-semibold tracking-tight">MedSaaS</span>
          )}
        </div>

        <nav className="flex flex-1 flex-col gap-1 p-2">
          <HoverCard openDelay={80} closeDelay={120}>
            <HoverCardTrigger asChild>
              <button
                type="button"
                className={cn(
                  itemBase,
                  "w-full text-left",
                  collapsed && "justify-center px-0",
                  dashboardActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
                aria-label="Dashboard"
              >
                <LayoutDashboard className="h-4 w-4 shrink-0" />
                {!collapsed && <span>Dashboard</span>}
              </button>
            </HoverCardTrigger>
            <HoverCardContent side="right" align="start" className="w-56 p-2">
              <p className="px-2 pb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Dashboards
              </p>
              <ul className="space-y-1">
                {DASHBOARDS.map(({ to, label, icon: Icon }) => (
                  <li key={to}>
                    <NavLink
                      to={to}
                      end
                      className={({ isActive }) =>
                        cn(
                          itemBase,
                          isActive
                            ? "bg-primary/10 text-primary"
                            : "text-foreground hover:bg-muted",
                        )
                      }
                    >
                      <Icon className="h-4 w-4" />
                      <span>{label}</span>
                      <span className="ml-auto text-[10px] uppercase tracking-wider text-muted-foreground">
                        Dev
                      </span>
                    </NavLink>
                  </li>
                ))}
              </ul>
            </HoverCardContent>
          </HoverCard>

          {MODULES.map(({ to, label, icon }) => renderItem(to, label, icon))}
        </nav>

        <div className="border-t p-2">
          <button
            type="button"
            onClick={() => setCollapsed((c) => !c)}
            className={cn(
              itemBase,
              "w-full text-muted-foreground hover:bg-muted hover:text-foreground",
              collapsed && "justify-center px-0",
            )}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <>
                <ChevronLeft className="h-4 w-4" />
                <span>Collapse</span>
              </>
            )}
          </button>
        </div>
      </aside>
    </TooltipProvider>
  );
}
