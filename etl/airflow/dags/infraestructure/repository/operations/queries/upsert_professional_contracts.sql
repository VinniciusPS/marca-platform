INSERT INTO operations.professional_contracts (
    professional_id,
    specialty,
    weekly_hours_contracted,
    weekly_fixed_cost,
    service_price,
    variable_cost_per_service,
    be_threshold_units
)
VALUES (
    :professional_id,
    :specialty,
    :weekly_hours_contracted,
    :weekly_fixed_cost,
    :service_price,
    :variable_cost_per_service,
    :be_threshold_units
)
ON CONFLICT (professional_id) DO UPDATE SET
    specialty = EXCLUDED.specialty,
    weekly_hours_contracted = EXCLUDED.weekly_hours_contracted,
    weekly_fixed_cost = EXCLUDED.weekly_fixed_cost,
    service_price = EXCLUDED.service_price,
    variable_cost_per_service = EXCLUDED.variable_cost_per_service,
    be_threshold_units = EXCLUDED.be_threshold_units;
