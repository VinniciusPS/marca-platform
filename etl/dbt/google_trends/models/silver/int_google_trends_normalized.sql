with source as (
    select * from {{ source('staging_source', 'stg_google_trends') }}
),
specialties as (
    select * from {{ source('clinic_source', 'specialties') }}
)

select
    s.specialty_id,
    src.keyword,
    src.interest as trend_score,
    src.source_date::date as reference_date
from source src
left join specialties s on lower(src.specialty) = lower(s.name)