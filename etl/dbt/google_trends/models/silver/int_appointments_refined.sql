with appointments as (
    select * from {{ source('clinic_source', 'appointments') }}
),

schedules as (
    select * from {{ source('clinic_source', 'professional_schedules') }}
),

exceptions as (
    select * from {{ source('clinic_source', 'schedule_exceptions') }}
),

-- 1. Calcula as horas ocupadas por profissional/dia
booked_hours as (
    select
        professional_id,
        appointment_date,
        sum(extract(epoch from (end_time - start_time)) / 3600) as hours_booked
    from appointments
    where status in ('completed', 'scheduled')
    group by 1, 2
),

-- 2. Calcula a capacidade teórica da grade semanal
theoretical_capacity as (
    select
        professional_id,
        day_of_week,
        sum(extract(epoch from (end_time - start_time)) / 3600) as daily_capacity_hours
    from schedules
    group by 1, 2
),

-- 3. Identifica horas bloqueadas por exceções (Férias/Folgas)
blocked_hours as (
    select
        professional_id,
        start_datetime::date as exception_date,
        sum(extract(epoch from (end_datetime - start_datetime)) / 3600) as hours_blocked
    from exceptions
    group by 1, 2
),

-- 4. Consolida Ocupação vs Capacidade Líquida
final_refinement as (
    select
        b.professional_id,
        b.appointment_date as reference_date,
        p.specialty_id,
        b.hours_booked,
        -- Capacidade Líquida = (Capacidade da Grade) - (Horas Bloqueadas)
        coalesce(t.daily_capacity_hours, 0) - coalesce(ex.hours_blocked, 0) as net_capacity_hours,
        case 
            when (coalesce(t.daily_capacity_hours, 0) - coalesce(ex.hours_blocked, 0)) <= 0 then 0
            else (b.hours_booked / (coalesce(t.daily_capacity_hours, 0) - coalesce(ex.hours_blocked, 0))) * 100 
        end as occupancy_rate
    from booked_hours b
    left join {{ source('clinic_source', 'professionals') }} p on b.professional_id = p.professional_id
    left join theoretical_capacity t on b.professional_id = t.professional_id 
        and extract(dow from b.appointment_date) = t.day_of_week
    left join blocked_hours ex on b.professional_id = ex.professional_id 
        and b.appointment_date = ex.exception_date
)

select * from final_refinement