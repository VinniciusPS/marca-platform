INSERT INTO marketing.marketing_search_terms (specialty_id, search_term)
VALUES (:specialty_id, :search_term)
ON CONFLICT (specialty_id, search_term) DO NOTHING;
