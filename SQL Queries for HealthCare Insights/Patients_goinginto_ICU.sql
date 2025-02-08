USE health;

SELECT 
    Admit_Month_Year,
    COUNT(Patient_ID) AS Patients_Going_To_ICU
    
FROM 
    healthcare_insights
WHERE
    Admit_Month_Year LIKE '%2023%'
    AND Bed_Occupancy = 'ICU'
GROUP BY
    Bed_Occupancy, Admit_Month_Year
ORDER BY
    STR_TO_DATE(Admit_Month_Year, '%M-%Y');
    
