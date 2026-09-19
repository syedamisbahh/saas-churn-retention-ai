import sqlite3
import pandas as pd

conn = sqlite3.connect('churn.db')

# --- Query 1: Overall churn rate ---
overall_churn = pd.read_sql_query("""
    SELECT Churn, COUNT(*) AS customer_count,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total
    FROM customers GROUP BY Churn;
""", conn)
overall_churn.to_csv('exports/overall_churn.csv', index=False)

# --- Query 2: MRR at risk ---
mrr_at_risk = pd.read_sql_query("""
    SELECT
      ROUND(SUM(MonthlyCharges), 2) AS total_mrr,
      ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_lost_to_churn,
      ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) / SUM(MonthlyCharges), 2) AS pct_mrr_at_risk
    FROM customers;
""", conn)
mrr_at_risk.to_csv('exports/mrr_at_risk.csv', index=False)

# --- Query 3: Churn by contract type ---
churn_by_contract = pd.read_sql_query("""
    SELECT Contract, COUNT(*) AS total,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
        ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
    FROM customers GROUP BY Contract ORDER BY churn_rate_pct DESC;
""", conn)
churn_by_contract.to_csv('exports/churn_by_contract.csv', index=False)

# --- Query 4: Churn by tenure bucket ---
churn_by_tenure_bucket = pd.read_sql_query("""
    SELECT
      CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49+ months'
      END AS tenure_bucket,
      COUNT(*) AS total,
      SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
      ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
    FROM customers GROUP BY tenure_bucket ORDER BY tenure_bucket;
""", conn)
churn_by_tenure_bucket.to_csv('exports/churn_by_tenure_bucket.csv', index=False)

# --- Query 5: Churn by TechSupport ---
churn_by_techsupport = pd.read_sql_query("""
    SELECT TechSupport, COUNT(*) AS total,
        ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
    FROM customers GROUP BY TechSupport;
""", conn)
churn_by_techsupport.to_csv('exports/churn_by_techsupport.csv', index=False)

# --- Query 6: Churn by OnlineSecurity ---
churn_by_onlinesecurity = pd.read_sql_query("""
    SELECT OnlineSecurity, COUNT(*) AS total,
        ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
    FROM customers GROUP BY OnlineSecurity;
""", conn)
churn_by_onlinesecurity.to_csv('exports/churn_by_onlinesecurity.csv', index=False)

# --- Query 7: Churn by DeviceProtection ---
churn_by_deviceprotection = pd.read_sql_query("""
    SELECT DeviceProtection, COUNT(*) AS total,
        ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
    FROM customers GROUP BY DeviceProtection;
""", conn)
churn_by_deviceprotection.to_csv('exports/churn_by_deviceprotection.csv', index=False)

# --- Query 8: Churn by payment method ---
churn_by_paymentmethod = pd.read_sql_query("""
    SELECT PaymentMethod, COUNT(*) AS total,
        ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
    FROM customers GROUP BY PaymentMethod ORDER BY churn_rate_pct DESC;
""", conn)
churn_by_paymentmethod.to_csv('exports/churn_by_paymentmethod.csv', index=False)

# --- Query 9: Retention by tenure ---
retention_by_tenure = pd.read_sql_query("""
    SELECT tenure, COUNT(*) AS customers_at_this_tenure,
        SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained,
        ROUND(100.0 * SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) / COUNT(*), 2) AS retention_rate_pct
    FROM customers GROUP BY tenure ORDER BY tenure;
""", conn)
retention_by_tenure.to_csv('exports/retention_by_tenure.csv', index=False)

# --- Query 10: High-value churned customers ---
high_value_at_risk = pd.read_sql_query("""
    SELECT customerID, MonthlyCharges, tenure, Contract, Churn
    FROM customers
    WHERE Churn = 'Yes' AND MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customers)
    ORDER BY MonthlyCharges DESC
    LIMIT 20;
""", conn)
high_value_at_risk.to_csv('exports/high_value_at_risk.csv', index=False)

conn.close()
print("All 10 exports done. Check the /exports folder.")