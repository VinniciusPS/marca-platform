UPDATE control.etl_load 
SET 
    status = :status, 
    end_time = :end_time,
    rows_extracted = :rows_extracted,
    rows_loaded = :rows_loaded,
    last_extracted_at = CURRENT_TIMESTAMP,
    error_message = :error_message
WHERE id = :id;