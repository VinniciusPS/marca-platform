INSERT INTO staging.stg_google_trends (
    source_date, keyword, group_name, specialty,
    interest, created_at, updated_at
)
VALUES (
    :source_date,
    :keyword,
    :group_name,
    :specialty,
    :interest,
    :created_at,
    :updated_at
)
ON CONFLICT (source_date, keyword, group_name)
DO UPDATE SET
    interest = EXCLUDED.interest,
    updated_at = EXCLUDED.updated_at;