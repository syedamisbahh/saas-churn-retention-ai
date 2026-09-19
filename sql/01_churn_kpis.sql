-- Overall churn rate
SELECT
  Churn,
  COUNT(*) AS customer_count,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total
FROM customers
GROUP BY Churn;


-- MRR at risk
SELECT
  ROUND(SUM(MonthlyCharges), 2) AS total_mrr,
  ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_lost_to_churn,
  ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) / SUM(MonthlyCharges), 2) AS pct_mrr_at_risk
FROM customers;