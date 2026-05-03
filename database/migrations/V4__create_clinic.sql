CREATE SCHEMA IF NOT EXISTS clinic;
---
--- 1. DOMÍNIO DE ESPECIALIDADES E MARKETING
---
CREATE TABLE IF NOT EXISTS clinic.specialties (
    specialty_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinic.marketing_search_terms (
    term_id SERIAL PRIMARY KEY,
    specialty_id INTEGER NOT NULL REFERENCES clinic.specialties(specialty_id),
    search_term TEXT NOT NULL
);

---
--- 2. DOMÍNIO DE PROFISSIONAIS E DISPONIBILIDADE
---
CREATE TABLE IF NOT EXISTS clinic.professionals (
    professional_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    document_type TEXT NOT NULL CHECK (document_type IN ('CRM', 'CPF')),
    document_number TEXT NOT NULL UNIQUE,
    specialty_id INTEGER NOT NULL REFERENCES clinic.specialties(specialty_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinic.professional_schedules (
    schedule_id SERIAL PRIMARY KEY,
    professional_id INTEGER NOT NULL REFERENCES clinic.professionals(professional_id),
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), 
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_time_range CHECK (start_time < end_time)
);

CREATE TABLE IF NOT EXISTS clinic.schedule_exceptions (
    exception_id SERIAL PRIMARY KEY,
    professional_id INTEGER NOT NULL REFERENCES clinic.professionals(professional_id),
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---
--- 3. DOMÍNIO DE OPERAÇÃO E PACIENTES
---
CREATE TABLE IF NOT EXISTS clinic.patients (
    patient_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinic.cid_codes (
    cid_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS clinic.services (
    service_id SERIAL PRIMARY KEY,
    specialty_id INTEGER NOT NULL REFERENCES clinic.specialties(specialty_id),
    service_name TEXT NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinic.appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES clinic.patients(patient_id),
    professional_id INTEGER NOT NULL REFERENCES clinic.professionals(professional_id),
    service_id INTEGER NOT NULL REFERENCES clinic.services(service_id),
    cid_id INTEGER NOT NULL REFERENCES clinic.cid_codes(cid_id),
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    final_price DECIMAL(10, 2), -- Valor real para cálculo de ROI (PJ)
    status TEXT NOT NULL DEFAULT 'scheduled' 
        CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show', 'inquiry')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fundamental para Lead Time (ML)
);

---
--- 5. ÍNDICES DE ALTA PERFORMANCE (DBT & ML)
---
CREATE INDEX IF NOT EXISTS idx_app_analytics ON clinic.appointments(appointment_date, professional_id, status);
CREATE INDEX IF NOT EXISTS idx_app_created_at ON clinic.appointments(created_at);
CREATE INDEX IF NOT EXISTS idx_sched_analytics ON clinic.professional_schedules(professional_id, day_of_week);
