-- High-value churned customers (above-average MonthlyCharges)
SELECT customerID, MonthlyCharges, tenure, Contract, Churn
FROM customers
WHERE Churn = 'Yes' AND MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customers)
ORDER BY MonthlyCharges DESC
LIMIT 20;