INSERT INTO clinic.appointments (
    patient_id, professional_id, service_id, cid_id,
    appointment_date, start_time, end_time,
    final_price, status, created_at
)
VALUES (
    :patient_id, :professional_id, :service_id, :cid_id,
    :appointment_date, :start_time, :end_time,
    :final_price, :status, CURRENT_TIMESTAMP
)
ON CONFLICT (patient_id, professional_id, appointment_date, start_time) DO UPDATE SET
    service_id = EXCLUDED.service_id,
    cid_id = EXCLUDED.cid_id,
    end_time = EXCLUDED.end_time,
    final_price = EXCLUDED.final_price,
    status = EXCLUDED.status;
