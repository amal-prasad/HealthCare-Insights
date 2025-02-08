USE health;

WITH FormattedData AS (
    SELECT 
        DATE_FORMAT(Admit_Date, '%Y-%m') AS Month_Year,  -- YYYY-MM format for correct sorting
        Diagnosis
    FROM 
        healthcare_insights
)
SELECT 
    Month_Year,
    Diagnosis,
    COUNT(*) AS Patient_Count
FROM 
    FormattedData
GROUP BY 
    Month_Year, Diagnosis
ORDER BY 
    Month_Year; 


