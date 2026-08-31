INSERT INTO clinic.schedule_exceptions (professional_id, start_datetime, end_datetime, reason, created_at)
VALUES (:professional_id, :start_datetime, :end_datetime, :reason, CURRENT_TIMESTAMP)
ON CONFLICT (professional_id, start_datetime, end_datetime) DO UPDATE SET
    reason = EXCLUDED.reason;
