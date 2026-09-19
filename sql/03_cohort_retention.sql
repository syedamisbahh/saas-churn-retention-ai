-- Retention by tenure (proxy — no signup date in this
-- dataset, so this is not a true monthly cohort curve)
SELECT
  tenure,
  COUNT(*) AS customers_at_this_tenure,
  SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained,
  ROUND(100.0 * SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) / COUNT(*), 2) AS retention_rate_pct
FROM customers
GROUP BY tenure
ORDER BY tenure;