USE health;

SELECT
    Diagnosis,
    Test AS Test_Type,
    COUNT(Test) AS Total_Tests
FROM
    healthcare_insights
GROUP BY
    Diagnosis, Test
ORDER BY
    Diagnosis, COUNT(Test) DESC;