USE Health;

SELECT 
    Diagnosis,
    COUNT(Patient_ID)
FROM 
    healthcare_insights
GROUP BY
    Diagnosis;