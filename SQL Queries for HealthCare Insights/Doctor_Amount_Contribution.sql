USE health;

SELECT
    Doctor,
    SUM(`Billing Amount`)
FROM
    healthcare_insights
GROUP BY
    Doctor
ORDER BY
    SUM(`Billing Amount`) DESC;