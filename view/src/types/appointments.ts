export type AppointmentStatus =
  | "scheduled"
  | "completed"
  | "cancelled"
  | "no_show";

export interface Appointment {
  appointment_id: number;
  patient_id: number;
  professional_id: number;
  service_id: number;
  cid_id: number;
  appointment_date: string; // ISO date (YYYY-MM-DD)
  start_time: string; // HH:mm:ss
  end_time: string; // HH:mm:ss
  final_price: number | null;
  status: AppointmentStatus | string;
  created_at: string; // ISO timestamp
}

export interface AppointmentFilters {
  date?: string; // YYYY-MM-DD
  statuses?: string[];
}

export interface Specialty {
  id: number;
  name: string;
}

export interface Professional {
  id: number;
  name: string;
  specialty_id: number;
}

export interface Service {
  id: number;
  name: string;
  price: number;
}

export interface NewAppointmentInput {
  specialty_id: number;
  professional_id: number;
  appointment_date: string;
  service_id: number;
}
