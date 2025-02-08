USE health;

SELECT
    Diagnosis,
    AVG(Followup_Duration) AS Average_Followup_Duration
FROM
    healthcare_insights
GROUP BY
     Diagnosis
ORDER BY
     Diagnosis;