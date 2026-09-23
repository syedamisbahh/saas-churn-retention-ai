# STEP 1: Load risk scores and original customer data
import pandas as pd
import sqlite3

conn = sqlite3.connect('churn.db')
customers = pd.read_sql_query("SELECT * FROM customers", conn)
conn.close()

risk_scores = pd.read_csv('exports/churn_scores.csv')

# Merge risk scores with full customer details
merged = customers.merge(risk_scores, on='customerID')

# Take the top 10 highest-risk ACTIVE customers (not already churned)
top_at_risk = merged[merged['Churn'] == 'No'].sort_values(
    by='churn_probability', ascending=False
).head(10)

print(top_at_risk[['customerID', 'churn_probability', 'Contract', 'tenure', 'InternetService']])

# STEP 2: Set up the Groq client
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# STEP 3: Build a grounded prompt per customer
def build_prompt(row):
    return f"""You are a Customer Success analyst assistant. Based ONLY on the customer 
data provided below, explain in 2 sentences why this customer is likely to churn — 
you MUST reference their internet service type if it's Fiber optic, since this is 
the single strongest churn driver identified by the underlying model — and recommend 
ONE specific, actionable retention step. Do not invent information not provided below.

Customer data:
- Contract type: {row['Contract']}
- Tenure: {row['tenure']} months
- Monthly charges: ${row['MonthlyCharges']}
- Internet service: {row['InternetService']}
- Tech support: {row['TechSupport']}
- Online security: {row['OnlineSecurity']}
- Payment method: {row['PaymentMethod']}
- Predicted churn probability: {round(row['churn_probability']*100, 1)}%

Respond in this exact format:
Explanation: <your explanation>
Recommended Action: <your recommendation>
"""

# STEP 4: Generate explanations for each at-risk customer
results = []

for _, row in top_at_risk.iterrows():
    prompt = build_prompt(row)
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    output = response.choices[0].message.content
    
    results.append({
        'customerID': row['customerID'],
        'churn_probability': row['churn_probability'],
        'ai_output': output
    })
    
    print(f"Processed {row['customerID']}")

# STEP 5: Save results
results_df = pd.DataFrame(results)
results_df.to_csv('exports/ai_retention_recommendations.csv', index=False)
print("\nSaved ai_retention_recommendations.csv")