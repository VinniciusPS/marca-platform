-- V1__init_schemas_and_test_table.sql

-- Schemas base (camada lakehouse simplificada)
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Tabela de teste na camada staging (efêmera)
CREATE TABLE IF NOT EXISTS staging.test_events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Seed de teste
INSERT INTO staging.test_events (event_name)
VALUES
    ('init_event_1'),
    ('init_event_2'),
    ('init_event_3'),
    ('init_event_4'),
    ('init_event_5');