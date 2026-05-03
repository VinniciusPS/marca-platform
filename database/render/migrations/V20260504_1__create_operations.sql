CREATE TABLE operations.professional_contracts (
    professional_id INT,
    specialty VARCHAR(50),
    weekly_hours_contracted INT,
    weekly_fixed_cost DECIMAL(10,2),
    service_price DECIMAL(10,2),
    variable_cost_per_service DECIMAL(10,2), 
    be_threshold_units INT 
);