USE health;

SELECT 
    Doctor,
    Test,
    COUNT(*) as TestCount
FROM healthcare_insights
GROUP BY Doctor, Test
ORDER BY Doctor, TestCount DESC;