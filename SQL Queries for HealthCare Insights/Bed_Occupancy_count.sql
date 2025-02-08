USE health;

SELECT 
    Bed_Occupancy,
    COUNT(Bed_Occupancy) AS Occupancy_Count    
FROM 
    healthcare_insights    
GROUP BY
    Bed_Occupancy
;