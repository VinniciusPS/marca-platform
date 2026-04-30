CREATE SCHEMA IF NOT EXISTS control;

CREATE TABLE IF NOT EXISTS control.etl_load (
    id BIGSERIAL PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    status TEXT NOT NULL, 
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    last_extracted_at TIMESTAMP, 
    rows_extracted INTEGER,
    rows_loaded INTEGER,
    error_message TEXT,
    CONSTRAINT etl_load_status_check
        CHECK (status IN ('running', 'success', 'failed'))
);

CREATE INDEX idx_etl_load_dataset
    ON control.etl_load (dataset_name);

CREATE INDEX idx_etl_load_status
    ON control.etl_load (status);

CREATE INDEX idx_etl_load_last_extracted
    ON control.etl_load (last_extracted_at);