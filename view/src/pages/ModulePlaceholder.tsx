import { Construction } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";

export default function ModulePlaceholder({ title }: { title: string }) {
  return (
    <AppShell>
      <main className="flex flex-1 items-center justify-center p-10">
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
            <Construction className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-semibold">{title}</h1>
          <p className="text-sm text-muted-foreground">
            Módulo em desenvolvimento.
          </p>
        </div>
      </main>
    </AppShell>
  );
}
