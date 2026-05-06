import type { ReactNode } from "react";
import { ModuleSideNav } from "./ModuleSideNav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen w-full bg-background">
      <ModuleSideNav />
      <div className="flex flex-1 min-w-0">{children}</div>
    </div>
  );
}
