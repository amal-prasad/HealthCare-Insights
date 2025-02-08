USE Healthcare;

SELECT 
    MIN(`Health Insurance Amount`) AS Health_Insurance_Amount,
    MAX(`Health Insurance Amount`) AS Health_Insurance_Amount,
    AVG(`Health Insurance Amount`) AS Average_Health_Insurance_Amount
FROM 
    healthcare_insights;