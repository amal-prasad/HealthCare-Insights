USE health;

WITH AmountStay AS (
    SELECT         
        `Billing Amount` / Admit_Stay AS BillingAmount_per_Day
    FROM
        healthcare_insights
)
SELECT
    AVG(BillingAmount_per_Day) AS Average_BillingAmount_per_Day,
    MAX(BillingAmount_per_Day) AS Max_BillingAmount_per_Day,
    MIN(BillingAmount_per_Day) AS Min_BillingAmount_per_Day
FROM
    AmountStay;