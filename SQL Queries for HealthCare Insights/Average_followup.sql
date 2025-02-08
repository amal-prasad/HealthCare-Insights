USE health;

SELECT
    MIN(Followup_Duration) AS Followup_Duration_Minimum,
    AVG(Followup_Duration) AS Followup_Duration_Average,
    MAX(Followup_Duration) AS Followup_Duration_Maximum
FROM
    healthcare_insights;
