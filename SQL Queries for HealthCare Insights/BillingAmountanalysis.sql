USE Health;

SELECT 
    MIN(`Billing Amount`) AS Min_Billing_Amount,
    MAX(`Billing Amount`) AS Max_Billing_Amount,
    AVG(`Billing Amount`) AS Average_Billing_Amount
FROM 
    healthcare_insights;