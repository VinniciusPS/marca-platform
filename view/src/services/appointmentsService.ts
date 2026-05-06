import type {
  Appointment,
  NewAppointmentInput,
  Professional,
  Service,
  Specialty,
} from "@/types/appointments";
import { apiFetch } from "./api";

/**
 * Mocked data — to be replaced by FastAPI endpoints:
 *   GET  /appointments
 *   POST /appointments
 *   GET  /specialties
 *   GET  /professionals?specialty_id=
 *   GET  /services
 *   GET  /professionals/:id/availability
 */
const MOCK_APPOINTMENTS: Appointment[] = Array.from({ length: 12 }, (_, i) => ({
  appointment_id: i + 1,
  patient_id: 1,
  professional_id: 1,
  service_id: 1,
  cid_id: 1,
  appointment_date: "2026-05-04",
  start_time: "14:00:00",
  end_time: "15:00:00",
  final_price: 180.0,
  status: "scheduled",
  created_at: "2026-05-04 02:03:23.624861",
}));

const MOCK_SPECIALTIES: Specialty[] = [
  { id: 1, name: "Nutrição" },
  { id: 2, name: "Cardiologia" },
  { id: 3, name: "Pediatria" },
  { id: 4, name: "Dermatologia" },
];

const MOCK_PROFESSIONALS: Professional[] = [
  { id: 1, name: "Dra. Ana Souza", specialty_id: 1 },
  { id: 2, name: "Dr. Bruno Lima", specialty_id: 1 },
  { id: 3, name: "Dr. Carlos Mendes", specialty_id: 2 },
  { id: 4, name: "Dra. Diana Rocha", specialty_id: 3 },
  { id: 5, name: "Dra. Elisa Castro", specialty_id: 4 },
];

const MOCK_SERVICES: Service[] = [
  { id: 1, name: "Consulta Inicial", price: 180.0 },
  { id: 2, name: "Retorno", price: 90.0 },
  { id: 3, name: "Avaliação Completa", price: 250.0 },
];

const USE_MOCK = (import.meta.env.VITE_USE_MOCK ?? "true") === "true";

const delay = (ms = 200) => new Promise((r) => setTimeout(r, ms));

export const appointmentsService = {
  async list(): Promise<Appointment[]> {
    if (USE_MOCK) {
      await delay();
      return MOCK_APPOINTMENTS;
    }
    return apiFetch<Appointment[]>("/appointments");
  },

  async create(input: NewAppointmentInput): Promise<Appointment> {
    if (USE_MOCK) {
      await delay();
      const next: Appointment = {
        appointment_id: MOCK_APPOINTMENTS.length + 1,
        patient_id: 1,
        professional_id: input.professional_id,
        service_id: input.service_id,
        cid_id: 1,
        appointment_date: input.appointment_date,
        start_time: "14:00:00",
        end_time: "15:00:00",
        final_price:
          MOCK_SERVICES.find((s) => s.id === input.service_id)?.price ?? null,
        status: "scheduled",
        created_at: new Date().toISOString(),
      };
      MOCK_APPOINTMENTS.push(next);
      return next;
    }
    return apiFetch<Appointment>("/appointments", {
      method: "POST",
      body: JSON.stringify(input),
    });
  },

  async listSpecialties(): Promise<Specialty[]> {
    if (USE_MOCK) {
      await delay(100);
      return MOCK_SPECIALTIES;
    }
    return apiFetch<Specialty[]>("/specialties");
  },

  async listProfessionals(specialtyId?: number): Promise<Professional[]> {
    if (USE_MOCK) {
      await delay(100);
      return specialtyId
        ? MOCK_PROFESSIONALS.filter((p) => p.specialty_id === specialtyId)
        : MOCK_PROFESSIONALS;
    }
    const qs = specialtyId ? `?specialty_id=${specialtyId}` : "";
    return apiFetch<Professional[]>(`/professionals${qs}`);
  },

  async listServices(): Promise<Service[]> {
    if (USE_MOCK) {
      await delay(100);
      return MOCK_SERVICES;
    }
    return apiFetch<Service[]>("/services");
  },

  /**
   * Returns the set of dates (YYYY-MM-DD) where the professional has free agenda.
   * Mocked: every weekday for the next 60 days is considered free.
   */
  async getAvailability(_professionalId: number): Promise<string[]> {
    if (USE_MOCK) {
      await delay(100);
      const out: string[] = [];
      const today = new Date();
      for (let i = 0; i < 60; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        const dow = d.getDay();
        if (dow !== 0 && dow !== 6) {
          out.push(d.toISOString().slice(0, 10));
        }
      }
      return out;
    }
    return apiFetch<string[]>(`/professionals/${_professionalId}/availability`);
  },
};
