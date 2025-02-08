USE health;

SELECT
    Diagnosis,
    AVG(Admit_Stay) AS Average_Stay
FROM
    healthcare_insights
GROUP BY
    Diagnosis;