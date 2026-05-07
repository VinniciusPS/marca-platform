{{ config(materialized='view') }}

WITH appointment_counts AS (
    -- Contagem de agendamentos por profissional na semana
    SELECT 
        professional_id,
        COUNT(appointment_id) AS total_appointments
    FROM {{ source('clinic', 'appointments') }}
    WHERE status IN ('scheduled', 'completed')
    -- Aqui você aplicaria o filtro de data para a semana vigente
    GROUP BY 1
),

contract_analysis AS (
    SELECT 
        p.name AS professional_name,
        c.specialty,
        c.weekly_fixed_cost,
        c.be_threshold_units,
        c.service_price,
        c.variable_cost_per_service,
        COALESCE(a.total_appointments, 0) AS actual_appointments,
        -- Margem bruta unitária: 180 - 20 = 160
        (c.service_price - c.variable_cost_per_service) AS margin_per_appointment
    FROM {{ source('operations', 'professional_contracts') }} c
    JOIN {{ source('clinic', 'professionals') }} p ON c.professional_id = p.professional_id
    LEFT JOIN appointment_counts a ON p.professional_id = a.professional_id
)

SELECT 
    *,
    -- Cálculo do Lucro Líquido Semanal: (160 * Qtd) - 2400
    (actual_appointments * margin_per_appointment) - weekly_fixed_cost AS weekly_net_profit,
    CASE 
        WHEN actual_appointments < be_threshold_units THEN '🚨 ABAIXO DO BE - Ociosidade Crítica'
        ELSE '✅ SAUDÁVEL - Meta Atingida'
    END AS actionable_insight
FROM contract_analysis