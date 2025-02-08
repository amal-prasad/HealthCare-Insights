USE health;

WITH AmountStay AS (
    SELECT 
        Bed_Occupancy,        
        `Billing Amount` / Admit_Stay AS BillingAmount_per_Room
        
    FROM
        healthcare_insights
)
SELECT
    Bed_Occupancy,
    AVG(BillingAmount_per_Room) AS Average_BillingAmount_per_Room,
    MAX(BillingAmount_per_Room) AS Max_BillingAmount_per_Room,
    MIN(BillingAmount_per_Room) AS Min_BillingAmount_per_Room
FROM
    AmountStay
GROUP BY
    Bed_Occupancy;