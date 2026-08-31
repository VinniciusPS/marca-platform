INSERT INTO clinic.cid_codes (code, description)
VALUES (:code, :description)
ON CONFLICT (code) DO NOTHING;
