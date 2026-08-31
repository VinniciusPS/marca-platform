-- Migration: Adição de constraint/índice de unicidade para suportar upserts no schema marketing

CREATE UNIQUE INDEX IF NOT EXISTS uq_marketing_search_terms_spec_term 
ON marketing.marketing_search_terms (specialty_id, search_term);

CREATE UNIQUE INDEX IF NOT EXISTS uq_marketing_benchmarks_specialty 
ON marketing.marketing_benchmarks (specialty);
