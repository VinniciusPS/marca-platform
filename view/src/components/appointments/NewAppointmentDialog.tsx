import { useEffect, useMemo, useState } from "react";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";
import {
  useAvailability,
  useCreateAppointment,
  useProfessionals,
  useServices,
  useSpecialties,
} from "@/hooks/useAppointments";

interface NewAppointmentDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function NewAppointmentDialog({
  open,
  onOpenChange,
}: NewAppointmentDialogProps) {
  const [specialtyId, setSpecialtyId] = useState<number | undefined>();
  const [professionalId, setProfessionalId] = useState<number | undefined>();
  const [date, setDate] = useState<Date | undefined>();
  const [serviceId, setServiceId] = useState<number | undefined>();

  const { data: specialties = [] } = useSpecialties();
  const { data: professionals = [] } = useProfessionals(specialtyId);
  const { data: services = [] } = useServices();
  const { data: availableDates = [] } = useAvailability(professionalId);
  const createMutation = useCreateAppointment();

  // Reset downstream fields when an upstream selection changes.
  useEffect(() => {
    setProfessionalId(undefined);
    setDate(undefined);
  }, [specialtyId]);

  useEffect(() => {
    setDate(undefined);
  }, [professionalId]);

  const availableSet = useMemo(
    () => new Set(availableDates),
    [availableDates],
  );

  const isDayAvailable = (d: Date) => availableSet.has(format(d, "yyyy-MM-dd"));

  const reset = () => {
    setSpecialtyId(undefined);
    setProfessionalId(undefined);
    setDate(undefined);
    setServiceId(undefined);
  };

  const handleClose = (next: boolean) => {
    if (!next) reset();
    onOpenChange(next);
  };

  const canSubmit =
    specialtyId !== undefined &&
    professionalId !== undefined &&
    date !== undefined &&
    serviceId !== undefined;

  const handleSubmit = async () => {
    if (!canSubmit) return;
    try {
      await createMutation.mutateAsync({
        specialty_id: specialtyId!,
        professional_id: professionalId!,
        appointment_date: format(date!, "yyyy-MM-dd"),
        service_id: serviceId!,
      });
      toast({ title: "Agendamento criado com sucesso" });
      handleClose(false);
    } catch (e) {
      toast({
        title: "Erro ao criar agendamento",
        description: e instanceof Error ? e.message : String(e),
        variant: "destructive",
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Novo agendamento</DialogTitle>
          <DialogDescription>
            Preencha os campos para agendar uma nova consulta.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-2">
          <div className="space-y-2">
            <Label>1. Especialidade</Label>
            <Select
              value={specialtyId?.toString() ?? ""}
              onValueChange={(v) => setSpecialtyId(Number(v))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecione a especialidade" />
              </SelectTrigger>
              <SelectContent>
                {specialties.map((s) => (
                  <SelectItem key={s.id} value={s.id.toString()}>
                    {s.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>2. Profissional</Label>
            <Select
              value={professionalId?.toString() ?? ""}
              onValueChange={(v) => setProfessionalId(Number(v))}
              disabled={specialtyId === undefined}
            >
              <SelectTrigger>
                <SelectValue
                  placeholder={
                    specialtyId === undefined
                      ? "Selecione antes a especialidade"
                      : "Selecione o profissional"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                {professionals.map((p) => (
                  <SelectItem key={p.id} value={p.id.toString()}>
                    {p.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>3. Data do agendamento</Label>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  disabled={professionalId === undefined}
                  className={cn(
                    "w-full justify-start text-left font-normal",
                    !date && "text-muted-foreground",
                  )}
                >
                  <CalendarIcon className="h-4 w-4" />
                  {date ? format(date, "dd/MM/yyyy") : "Escolher data"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={date}
                  onSelect={setDate}
                  disabled={(d) => !isDayAvailable(d)}
                  modifiers={{ available: (d) => isDayAvailable(d) }}
                  modifiersClassNames={{
                    available:
                      "bg-primary/15 text-primary hover:bg-primary/25",
                  }}
                  initialFocus
                  className={cn("p-3 pointer-events-auto")}
                />
                <p className="px-3 pb-3 text-xs text-muted-foreground">
                  Dias em azul indicam agenda livre.
                </p>
              </PopoverContent>
            </Popover>
          </div>

          <div className="space-y-2">
            <Label>4. Tipo de serviço</Label>
            <Select
              value={serviceId?.toString() ?? ""}
              onValueChange={(v) => setServiceId(Number(v))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecione o serviço" />
              </SelectTrigger>
              <SelectContent>
                {services.map((s) => (
                  <SelectItem key={s.id} value={s.id.toString()}>
                    {s.name} —{" "}
                    {s.price.toLocaleString("pt-BR", {
                      style: "currency",
                      currency: "BRL",
                    })}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => handleClose(false)}>
            Cancelar
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!canSubmit || createMutation.isPending}
          >
            {createMutation.isPending ? "Criando..." : "Criar agendamento"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
