USE health;

SELECT
    Test,
    COUNT(Patient_ID) AS Patients
FROM
    healthcare_insights
GROUP BY
    Test;
