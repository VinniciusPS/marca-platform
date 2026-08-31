-- Migration: Adição de constraints/índices de unicidade para suportar upserts no schema clinic

CREATE UNIQUE INDEX IF NOT EXISTS uq_services_specialty_name 
ON clinic.services (specialty_id, service_name);

CREATE UNIQUE INDEX IF NOT EXISTS uq_professional_schedules_prof_day 
ON clinic.professional_schedules (professional_id, day_of_week);

CREATE UNIQUE INDEX IF NOT EXISTS uq_schedule_exceptions_prof_time 
ON clinic.schedule_exceptions (professional_id, start_datetime, end_datetime);

CREATE UNIQUE INDEX IF NOT EXISTS uq_appointments_patient_prof_date_time 
ON clinic.appointments (patient_id, professional_id, appointment_date, start_time);
