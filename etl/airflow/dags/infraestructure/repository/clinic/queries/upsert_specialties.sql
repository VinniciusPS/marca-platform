INSERT INTO clinic.specialties (name, created_at)
VALUES (:name, CURRENT_TIMESTAMP)
ON CONFLICT (name) DO NOTHING;
