USE Health;

SELECT 
    MIN(Admit_Stay) AS Minimum_Stay,
    AVG(Admit_Stay) AS Average_Stay,
    MAX(Admit_Stay) AS Maximum_Stay
FROM 
    healthcare_insights;
