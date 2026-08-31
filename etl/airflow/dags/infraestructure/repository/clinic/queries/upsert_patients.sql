INSERT INTO clinic.patients (name, cpf, created_at)
VALUES (:name, :cpf, CURRENT_TIMESTAMP)
ON CONFLICT (cpf) DO UPDATE SET
    name = EXCLUDED.name;
