USE health;

SELECT
    Doctor,
    AVG(Feedback)
FROM
    healthcare_insights
GROUP BY
    Doctor;