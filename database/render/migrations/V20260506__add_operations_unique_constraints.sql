-- Migration: Adição de constraint/índice de unicidade para suportar upserts no schema operations

CREATE UNIQUE INDEX IF NOT EXISTS uq_professional_contracts_prof_id 
ON operations.professional_contracts (professional_id);
