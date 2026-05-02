INSERT INTO control.etl_load (dataset_name, status, start_time)
VALUES (:name, 'running', CURRENT_TIMESTAMP)
RETURNING id;