{{ config(materialized='view') }}

WITH trends_with_lag AS (
    -- Etapa 1: Calculamos o delta garantindo que o LAG tenha acesso ao histórico
    SELECT 
        specialty,
        source_date,
        interest,
        LAG(interest) OVER (PARTITION BY specialty ORDER BY source_date) AS previous_interest
    FROM {{ source('staging', 'stg_google_trends') }}
),

calculated_delta AS (
    -- Etapa 2: Calculamos o Delta Real e rankeamos por data para pegar o último
    SELECT 
        specialty,
        source_date,
        ((interest - previous_interest) / NULLIF(previous_interest, 0)) AS delta_interest,
        ROW_NUMBER() OVER (PARTITION BY specialty ORDER BY source_date DESC) AS latest_rank
    FROM trends_with_lag
),

latest_trends AS (
    -- Etapa 3: Filtramos apenas a última variação calculada
    SELECT 
        specialty,
        delta_interest
    FROM calculated_delta
    WHERE latest_rank = 1
),

marketing_logic AS (
    SELECT 
        b.specialty,
        b.base_cpc,
        b.base_cvr,
        b.elasticity_score,
        b.net_margin_limit,
        COALESCE(t.delta_interest, 0) AS current_delta,
        -- Fórmula: novo_cpc = cpc * (1 + (0.7 * delta_trends))
        b.base_cpc * (1 + (b.elasticity_score * COALESCE(t.delta_interest, 0))) AS calculated_cpc
    FROM {{ source('marketing', 'marketing_benchmarks') }} b
    LEFT JOIN latest_trends t ON b.specialty = t.specialty
)

SELECT 
    specialty,
    current_delta AS scenario_delta,
    ROUND(calculated_cpc, 2) AS novo_cpc,
    ROUND((calculated_cpc / base_cvr), 2) AS projected_cac,
    ROUND((net_margin_limit - (calculated_cpc / base_cvr)), 2) AS liquid_margin_after_cac,
    CASE 
        WHEN (calculated_cpc / base_cvr) < 80 THEN 'Agressividade Permitida'
        WHEN (calculated_cpc / base_cvr) = 80 THEN 'Limite de Operação (Break-even)'
        ELSE 'Bid Baixo / Combinar Canais Baratos'
    END AS mkt_strategy_status
FROM marketing_logic