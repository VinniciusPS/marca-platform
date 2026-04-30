INSERT INTO staging.stg_google_trends (
    source_date, keyword, group_name, specialty,
    interest, created_at, updated_at
)
VALUES (
    to_timestamp(:source_date), :keyword, :group_name, :specialty,
    :interest, to_timestamp(:ingestion_ts), :updated_at
)
ON CONFLICT (source_date, keyword, group_name)
DO UPDATE SET
    interest = EXCLUDED.interest,
    updated_at = CURRENT_TIMESTAMP;