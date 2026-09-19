import pandas as pd
import sqlite3

df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Fix a known quirk: TotalCharges is text with a few blanks for new customers
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

conn = sqlite3.connect('churn.db')
df.to_sql('customers', conn, if_exists='replace', index=False)
conn.close()

print("Import done.")