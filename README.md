# SaaS Churn Prediction & AI-Driven Retention System

An end-to-end analytics project that identifies at-risk SaaS customers, quantifies revenue at risk, and generates AI-powered retention recommendations.

---

## Business Problem

SaaS companies lose recurring revenue when at-risk customers churn without warning, often because manual monitoring can't keep pace with the volume of accounts. This project identifies the key drivers of churn, quantifies monthly recurring revenue (MRR) at risk, and recommends specific retention actions — proactively, before customers cancel rather than after.

## Objectives

- Identify the key drivers of customer churn
- Quantify monthly recurring revenue (MRR) at risk
- Predict which active customers are likely to churn
- Generate plain-English, actionable retention recommendations using AI
- Present findings in a business-facing, interactive dashboard

Full requirements and user stories are documented in [`/docs/BRD.md`](docs/BRD.md).

## Dataset

This project uses the public **Telco Customer Churn** dataset (Kaggle). While the raw data is from telecom, its subscription/contract/tenure structure closely mirrors SaaS churn patterns (month-to-month vs. annual contracts, recurring monthly billing, add-on services), so it's treated here as a SaaS retention case study.

Source: [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## Key Findings

- **Overall churn rate:** 26.54% of customers
- **MRR at risk:** $139,130.85 lost to churned customers (30.5% of total MRR)
- **Contract type is the strongest churn driver:** Month-to-month contracts churn at 42.71% vs. 11.27% for one-year and 2.83% for two-year contracts
- **New customers are highest-risk:** Customers with 0–12 months tenure churn at 47.44% vs. 9.51% for customers past 49 months
- **Missing add-on services correlate with churn:** Customers without Tech Support churn at 41.64% vs. 15.17% with it (similar pattern for Online Security and Device Protection)
- **Payment method signals risk:** Electronic check payers show the highest churn rate at 45.29%, notably higher than automatic payment methods
- **20 high-value customers** above average monthly spend churned in this dataset — see `sql/04_at_risk_customers.sql` (query) and `exports/high_value_at_risk.csv` (results)
- **Internet service type is a strong signal:** Fiber optic customers churn at 41.89% vs. 18.96% for DSL and just 7.4% for customers with no internet service — this is the model's single strongest churn-driving factor, and a clear candidate for retention investigation (e.g., service reliability, pricing, or bundling issues specific to fiber plans).

---

## Dashboard

![Dashboard Screenshot](dashboard/Screenshot.png)

**[View Interactive Dashboard on Tableau Public →](https://public.tableau.com/shared/3G64JYXZ8?:display_count=n&:origin=viz_share_link)**

### Chart Selection Rationale

Each visualization was chosen based on the type of relationship in the data, not visual preference:

| Chart | Used For | Why |
|---|---|---|
| Bar (horizontal) | Churn by Contract, Tenure Bucket, Services, Payment Method | Comparing discrete, unordered categories - bar charts let viewers judge relative magnitude accurately across groups |
| Line | Retention by Tenure | Tenure is continuous and sequential - a line reveals the rate of change in retention over time, which a bar chart would flatten and hide |
| Pie | Overall Churn | A simple two-way part-to-whole split; a pie chart communicates "proportion of a whole" faster than a two-bar comparison |
| Big number tile | MRR at Risk, Pct MRR at Risk | A single critical fact needs no visual encoding - clarity over decoration |
| Table | High-Value At-Risk Customers | Individual records with mixed attribute types (ID, tenure, contract, charge) — a table preserves every attribute without forcing a false chart reduction |

---

## Tech Stack

- **Python** (pandas, scikit-learn) — data cleaning and churn prediction model
- **SQLite** — data storage and querying
- **Tableau Public** — dashboard and visualization
- **[LLM provider — e.g. Google AI Studio / Groq]** — AI-generated risk explanations and retention recommendations

## Project Structure

```
├── sql/                  # Business-question queries
│   ├── 01_churn_kpis.sql
│   ├── 02_segmentation.sql
│   ├── 03_cohort_retention.sql
│   └── 04_at_risk_customers.sql
├── exports/              # CSV outputs feeding the dashboard
├── dashboard/            # Tableau workbook + screenshot
│   ├── churn_dashboard.twbx
│   └── screenshot.png
├── model/                # Trained model artifact
│   └── churn_model.pkl
├── docs/                 # BRD
│   └── BRD.md
├── main.py               # Data cleaning & import into SQLite
├── train_model.py        # Churn prediction model training and evaluation
├── requirements.txt
└── README.md
```

---

## Churn Prediction Model

A logistic regression model was trained to predict churn probability for each customer, using contract type, tenure, billing, and service-usage features. Logistic regression was chosen specifically for its interpretability - its coefficients directly show which factors increase or decrease churn risk, which the AI explanation layer relies on.

Data preparation:
- Categorical fields one-hot encoded (`drop_first=True` to avoid redundant columns)
- Numeric fields (`tenure`, `MonthlyCharges`, `TotalCharges`) standardized using `StandardScaler`, fit on the training set only to avoid data leakage into the test set
- 80/20 train/test split (`random_state=42` for reproducibility)

Performance (on held-out test data):
- Accuracy: 82.1%
- Precision: 68.6%
- Recall: 59.8%
- Confusion Matrix: `[[934, 102], [150, 223]]`

Top churn-driving factors: Fiber optic internet service, Total Charges, Streaming Movies subscription, Paperless Billing, Electronic Check payment method

Top churn-preventing factors: Two-year contract, longer tenure, one-year contract, active phone service, Online Security subscription

These findings are broadly consistent with the SQL-based segmentation analysis above, reinforcing that the model is learning genuine patterns rather than noise. One new finding surfaced by the model - Fiber optic internet service as a top churn driver - led to an additional SQL query (`sql/02_segmentation.sql`) to validate and explain it with real segmentation data.

## Limitations

- Retention-by-tenure is a proxy metric — the dataset has no signup date, so this groups customers by *how long they've been a customer so far* rather than a true monthly cohort curve.
- Built on a public dataset, not live company data.
- Churn prediction model is intentionally kept simple and interpretable (logistic regression) rather than a higher-accuracy black-box model, to support the AI explanation layer.
- Some engineered/raw features (`tenure`, `MonthlyCharges`, `TotalCharges`) are correlated with one another (`TotalCharges` ≈ `tenure` × `MonthlyCharges`), a form of multicollinearity that can make individual model coefficients less stable to interpret in isolation, even though overall model performance remains valid.
- The model currently misses roughly 40% of customers who actually churn (recall of 59.8%) — meaning a real deployment would need either a lower decision threshold or a more sensitive model if minimizing missed at-risk customers is the priority over minimizing false alarms.

## AI-Generated Retention Recommendations — [TODO]
Example input/output — a sample customer, their risk explanation, and the recommended action.