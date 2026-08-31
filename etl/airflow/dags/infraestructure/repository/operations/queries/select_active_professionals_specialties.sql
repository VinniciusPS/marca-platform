SELECT 
    p.professional_id, 
    s.name AS specialty
FROM clinic.professionals p
JOIN clinic.specialties s ON p.specialty_id = s.specialty_id
WHERE p.is_active = TRUE
ORDER BY p.professional_id ASC;
