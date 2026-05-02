-- cria a tabela staging.stg_google_trends para armazenar os dados brutos do Google Trends

CREATE TABLE IF NOT EXISTS staging.stg_google_trends (
    id BIGSERIAL PRIMARY KEY,

    source_date TIMESTAMP NOT NULL,
    keyword TEXT NOT NULL,
    group_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    interest INTEGER NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    CONSTRAINT stg_google_trends_uk
        UNIQUE (source_date, keyword, group_name)
);

-- índices para leitura e performance no dbt

CREATE INDEX IF NOT EXISTS idx_stg_gt_source_date
    ON staging.stg_google_trends (source_date);

CREATE INDEX IF NOT EXISTS idx_stg_gt_specialty
    ON staging.stg_google_trends (specialty);

CREATE INDEX IF NOT EXISTS idx_stg_gt_group
    ON staging.stg_google_trends (group_name);

CREATE INDEX IF NOT EXISTS idx_stg_gt_updated_at
    ON staging.stg_google_trends (updated_at);