import pandas as pd
import sqlite3

conn = sqlite3.connect('churn.db')
customers = pd.read_sql_query("SELECT * FROM customers", conn)
conn.close()

risk_scores = pd.read_csv('exports/churn_scores.csv')
merged = customers.merge(risk_scores, on='customerID')

# Only active customers (haven't already churned), above a risk threshold
at_risk_threshold = 0.5
high_risk_active = merged[
    (merged['Churn'] == 'No') & (merged['churn_probability'] >= at_risk_threshold)
]

total_at_risk_customers = len(high_risk_active)
total_at_risk_mrr = high_risk_active['MonthlyCharges'].sum()

print(f"Active customers above {at_risk_threshold*100:.0f}% churn risk: {total_at_risk_customers}")
print(f"Total MRR represented by these customers: ${total_at_risk_mrr:,.2f}")

# Scenario: if proactive outreach retains X% of flagged high-risk customers
scenarios = [0.10, 0.20, 0.30]

for retention_rate in scenarios:
    estimated_monthly_mrr_saved = total_at_risk_mrr * retention_rate
    estimated_annual_mrr_saved = estimated_monthly_mrr_saved * 12
    print(f"\nIf {retention_rate*100:.0f}% of flagged customers are retained:")
    print(f"  Estimated monthly MRR saved: ${estimated_monthly_mrr_saved:,.2f}")
    print(f"  Estimated annual impact: ${estimated_annual_mrr_saved:,.2f}")