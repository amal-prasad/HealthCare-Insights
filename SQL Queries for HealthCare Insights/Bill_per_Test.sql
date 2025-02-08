USE health;

WITH AmountStay AS (
    SELECT 
        Test,        
        `Billing Amount` / Admit_Stay AS BillingAmount_per_Test
        
    FROM
        healthcare_insights
)
SELECT
    Test,
    AVG(BillingAmount_per_Test) AS Average_BillingAmount_per_Test,
    MAX(BillingAmount_per_Test) AS Max_BillingAmount_per_Test,
    MIN(BillingAmount_per_Test) AS Min_BillingAmount_per_Test
FROM
    AmountStay
GROUP BY
    Test;