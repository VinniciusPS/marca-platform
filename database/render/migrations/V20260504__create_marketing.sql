CREATE SCHEMA IF NOT EXISTS marketing;

-- Tabela para termos de busca relacionados a cada especialidade (para análise de marketing)
CREATE TABLE IF NOT EXISTS marketing.marketing_search_terms (
    term_id SERIAL PRIMARY KEY,
    specialty_id INTEGER NOT NULL REFERENCES clinic.specialties(specialty_id),
    search_term TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marketing.marketing_benchmarks (
    specialty VARCHAR(50),
    base_cpc DECIMAL(10,4), 
    base_cvr DECIMAL(5,4),  
    elasticity_score DECIMAL(5,2), 
    net_margin_limit DECIMAL(10,2) 
);