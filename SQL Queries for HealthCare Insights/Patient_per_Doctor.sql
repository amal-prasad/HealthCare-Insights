USE health;

SELECT 
    DISTINCT Doctor,
    COUNT(Patient_ID)
FROM
    healthcare_insights
GROUP BY
    Doctor;