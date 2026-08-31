INSERT INTO clinic.services (specialty_id, service_name, base_price, created_at)
VALUES (:specialty_id, :service_name, :base_price, CURRENT_TIMESTAMP)
ON CONFLICT (specialty_id, service_name) DO UPDATE SET
    base_price = EXCLUDED.base_price;
