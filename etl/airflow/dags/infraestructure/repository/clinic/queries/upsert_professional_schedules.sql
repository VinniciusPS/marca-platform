INSERT INTO clinic.professional_schedules (professional_id, day_of_week, start_time, end_time, created_at)
VALUES (:professional_id, :day_of_week, :start_time, :end_time, CURRENT_TIMESTAMP)
ON CONFLICT (professional_id, day_of_week) DO NOTHING;
