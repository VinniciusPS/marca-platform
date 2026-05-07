import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "./pages/Index";
import Appointments from "./pages/Appointments";
import OperationsDashboard from "./pages/OperationsDashboard.tsx";
import ModulePlaceholder from "./pages/ModulePlaceholder";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/dashboard/operations" element={<OperationsDashboard />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/patients" element={<ModulePlaceholder title="Patients" />} />
          <Route path="/professionals" element={<ModulePlaceholder title="Professionals" />} />
          <Route path="/operations" element={<ModulePlaceholder title="Operations" />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
