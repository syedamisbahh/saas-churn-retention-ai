# Load data from SQLite
import pandas as pd
import sqlite3

conn = sqlite3.connect('churn.db')
df = pd.read_sql_query("SELECT * FROM customers", conn)
conn.close()

print(df.shape)
print(df.head())

#Clean columns
df = df.drop(columns=['customerID'])
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(0)

#  Convert target column to numbers
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Encode categorical columns
categorical_cols = df.select_dtypes(include='object').columns.tolist()
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Separate features (X) and target (y)
X = df_encoded.drop(columns=['Churn'])
y = df_encoded['Churn']

# Train/test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Under train/split - > Scale numeric features (fit on train only, apply to both)
from sklearn.preprocessing import StandardScaler

numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
scaler = StandardScaler()

X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

# Train the model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate the model
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Feature importance (coefficients)
coefficients = pd.DataFrame({
    'feature': X.columns,
    'coefficient': model.coef_[0]
}).sort_values(by='coefficient', ascending=False)

print("\nTop churn-driving factors:")
print(coefficients.head(10))
print("\nTop churn-preventing factors:")
print(coefficients.tail(10))

# Generate churn risk score per customer
X_scaled = X.copy()
X_scaled[numeric_cols] = scaler.transform(X_scaled[numeric_cols])

df_encoded['churn_probability'] = model.predict_proba(X_scaled)[:, 1]

conn = sqlite3.connect('churn.db')
ids = pd.read_sql_query("SELECT customerID FROM customers", conn)
conn.close()

df_encoded['customerID'] = ids['customerID']

df_encoded[['customerID', 'churn_probability']].sort_values(
    by='churn_probability', ascending=False
).to_csv('exports/churn_scores.csv', index=False)

print("\nSaved churn_scores.csv")

# Save the trained model
import joblib

joblib.dump(model, 'model/churn_model.pkl')

print("Saved churn_model.pkl")