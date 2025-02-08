USE Health;
SELECT 
    DATE_FORMAT(Admit_Date, '%Y-%m') AS Admit_Month_Year,
    COUNT(DISTINCT Patient_ID) AS Patient_Count
FROM 
    healthcare_insights
GROUP BY 
    DATE_FORMAT(Admit_Date, '%Y-%m')
ORDER BY 
    DATE_FORMAT(Admit_Date, '%Y-%m');
