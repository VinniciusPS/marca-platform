INSERT INTO clinic.professionals (name, document_type, document_number, specialty_id, is_active, created_at)
VALUES (:name, :document_type, :document_number, :specialty_id, :is_active, CURRENT_TIMESTAMP)
ON CONFLICT (document_number) DO UPDATE SET
    name = EXCLUDED.name,
    specialty_id = EXCLUDED.specialty_id,
    is_active = EXCLUDED.is_active;
