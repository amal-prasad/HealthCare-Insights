USE health;

WITH Datedifference AS (
    SELECT 
        Discharge_Date,
        `Followup Date`,
        DATEDIFF(`Followup Date`, Discharge_Date) AS Date_Difference
    FROM
        healthcare_insights
)
SELECT
    AVG(Date_Difference) AS Average_Difference,
    MAX(Date_Difference) AS Max_Difference,
    MIN(Date_Difference) AS Min_Difference
FROM
    Datedifference;
