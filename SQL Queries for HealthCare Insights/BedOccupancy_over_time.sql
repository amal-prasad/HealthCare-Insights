USE health;

SELECT 
    Admit_Month_Year,
    Bed_Occupancy,
    COUNT(Bed_Occupancy) AS Occupancy_Count
    
FROM 
    healthcare_insights
WHERE
    Admit_Month_Year LIKE '%2023%'
GROUP BY
    Bed_Occupancy, Admit_Month_Year
ORDER BY
    STR_TO_DATE(Admit_Month_Year, '%M-%Y');

