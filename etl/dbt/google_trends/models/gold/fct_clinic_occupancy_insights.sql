with occupancy as (
    -- Lógica simplificada de ocupação vinda da Silver
    select 
        specialty_id,
        reference_date,
        avg(occupancy_rate) as avg_occ
    from {{ ref('int_appointments_refined') }}
    group by 1, 2
),
trends as (
    select 
        specialty_id,
        reference_date,
        avg(trend_score) as avg_trend
    from {{ ref('int_google_trends_normalized') }}
    group by 1, 2
)

select
    o.specialty_id,
    o.reference_date,
    o.avg_occ as occupancy_rate,
    t.avg_trend as google_interest,
    case 
        when o.avg_occ < 60 and t.avg_trend > 70 then 'ESCALAR'
        when o.avg_occ < 60 and t.avg_trend <= 70 then 'OTIMIZAR'
        when o.avg_occ >= 85 and t.avg_trend > 70 then 'EXPANDIR'
        else 'ESTABILIDADE'
    end as insight_action
from occupancy o
left join trends t on o.specialty_id = t.specialty_id 
    and o.reference_date = t.reference_date