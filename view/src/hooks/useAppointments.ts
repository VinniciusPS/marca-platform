import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { appointmentsService } from "@/services/appointmentsService";
import type {
  Appointment,
  AppointmentFilters,
  NewAppointmentInput,
} from "@/types/appointments";

export function useAppointments() {
  return useQuery({
    queryKey: ["appointments"],
    queryFn: () => appointmentsService.list(),
    staleTime: 30_000,
  });
}

export function useSpecialties() {
  return useQuery({
    queryKey: ["specialties"],
    queryFn: () => appointmentsService.listSpecialties(),
    staleTime: 5 * 60_000,
  });
}

export function useProfessionals(specialtyId?: number) {
  return useQuery({
    queryKey: ["professionals", specialtyId],
    queryFn: () => appointmentsService.listProfessionals(specialtyId),
    enabled: specialtyId !== undefined,
    staleTime: 5 * 60_000,
  });
}

export function useServices() {
  return useQuery({
    queryKey: ["services"],
    queryFn: () => appointmentsService.listServices(),
    staleTime: 5 * 60_000,
  });
}

export function useAvailability(professionalId?: number) {
  return useQuery({
    queryKey: ["availability", professionalId],
    queryFn: () => appointmentsService.getAvailability(professionalId!),
    enabled: professionalId !== undefined,
    staleTime: 60_000,
  });
}

export function useCreateAppointment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: NewAppointmentInput) =>
      appointmentsService.create(input),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["appointments"] });
    },
  });
}

export function applyAppointmentFilters(
  data: Appointment[],
  filters: AppointmentFilters,
): Appointment[] {
  return data.filter((row) => {
    if (filters.date && row.appointment_date !== filters.date) return false;
    if (filters.statuses?.length && !filters.statuses.includes(row.status))
      return false;
    return true;
  });
}
