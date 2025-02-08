USE health;

WITH Datedifference AS (
    SELECT 
        `Billing Amount` AS Billing_Amount,
        `Health Insurance Amount` AS Insurance_Amount,
        (`Billing Amount` - `Health Insurance Amount`) AS Avg_Amount
    FROM
        healthcare_insights
)
SELECT 
    AVG(Avg_Amount) AS Average_Amount,
    MAX(Avg_Amount) AS Max_Difference,
    MIN(Avg_Amount) AS Min_Difference
FROM 
    Datedifference;