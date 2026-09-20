# Business Requirements Document (BRD)
## SaaS Churn Prediction & AI-Driven Retention System

**Document version:** 1.0
**Author:** Syeda Misbah Hussain
**Date:** 09/16/2026
**Status:** Draft

---

## 1. Business Problem

SaaS companies lose recurring revenue when at-risk customers churn without warning. Support and Customer Success teams typically identify churn risk reactively — after a customer has already cancelled or stopped engaging — because manual account monitoring cannot scale with the volume of active customers. This results in preventable revenue loss and missed opportunities for timely retention intervention.

## 2. Business Objective

Build a system that proactively identifies at-risk customers, quantifies the revenue impact of churn, and recommends specific, actionable retention steps — before a customer cancels, rather than after.

## 3. Scope

### In Scope
- Analysis of historical customer data to identify churn drivers
- Quantification of churn rate and monthly recurring revenue (MRR) at risk
- A predictive model to flag active customers likely to churn
- An AI-generated layer that explains each at-risk customer's risk factors and recommends a retention action, in plain business language
- A dashboard presenting churn KPIs, segmentation, and at-risk customers to a non-technical business stakeholder

### Out of Scope
- Live integration with a production billing or CRM system
- Automated execution of retention actions (e.g., auto-sending discount offers)
- Real-time (streaming) data processing
- A/B testing of retention strategies

## 4. Stakeholders

| Role | Interest / Concern |
|---|---|
| Customer Success Manager | Wants a prioritized list of at-risk accounts and a reason/action for each |
| Sales / Revenue Leadership | Wants to understand total MRR at risk and where it's concentrated |
| Data/Analytics Team | Wants a model that is interpretable and maintainable, not a black box |
| Compliance / Data Privacy | Wants assurance that any AI-driven customer profiling is explainable and does not use protected attributes unfairly |

## 5. Assumptions

- Historical customer data (contract type, tenure, billing, service usage, churn status) is available and reasonably complete.
- "Churn" is defined as a customer who has cancelled their subscription (matches the `Churn` field in the source dataset).
- The dataset used for this project (Telco Customer Churn, Kaggle) is a proxy for a SaaS company's customer base due to its comparable subscription/contract/tenure structure; findings are illustrative of the approach, not derived from a live SaaS company's real data.

## 6. Constraints

- No signup/join date is available in the dataset, so true cohort-based retention analysis (tracking a specific monthly cohort over time) is not possible. Tenure-based retention is used as a proxy instead.
- The predictive model must remain interpretable (e.g., logistic regression or decision tree) rather than a high-complexity black-box model, so that its outputs can be explained in plain language to a business stakeholder.

## 7. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | The system shall calculate the overall customer churn rate. |
| FR-02 | The system shall calculate monthly recurring revenue (MRR) and the portion of MRR attributable to churned customers. |
| FR-03 | The system shall segment churn rate by contract type, tenure, add-on services, and payment method. |
| FR-04 | The system shall predict a churn probability score for each active customer. |
| FR-05 | The system shall identify the top factors contributing to each customer's predicted churn risk. |
| FR-06 | The system shall generate a plain-English explanation of each at-risk customer's risk factors, using an AI language model. |
| FR-07 | The system shall generate a recommended retention action for each at-risk customer, using an AI language model. |
| FR-08 | The system shall present churn KPIs, segmentation breakdowns, and at-risk customers in an interactive dashboard. |
| FR-09 | The dashboard shall allow filtering of results by at least one dimension (e.g., contract type). |

## 8. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | The churn prediction model shall be interpretable (e.g., logistic regression or decision tree), with feature importances or coefficients available for explanation. | Directly discussed: an interpretable model is required so the Day 5 AI layer can explain *why* a customer was flagged, rather than working against a black box. |
| NFR-02 | Dashboard visuals shall be understandable by a non-technical business stakeholder (e.g., a Customer Success Manager) without requiring knowledge of the underlying SQL or data model. | Directly discussed: the dashboard's stated purpose throughout was to be usable by a business stakeholder, not just a technical audience — this was the reasoning behind every chart-type decision (Chart Selection Rationale). |
| NFR-03 | AI-generated explanations and retention recommendations shall be grounded in the model's actual feature importances or the customer's real data fields, and shall not fabricate reasons unsupported by the data. | Directly discussed: the plan to feed each customer's real risk score and top contributing factors into the LLM (Day 5), rather than open-ended generation, specifically to avoid hallucinated explanations. |
| NFR-04 | Customer data used in this project shall come only from a public, non-sensitive dataset; no real customer PII shall be used. | Directly discussed: the dataset disclosure and honesty requirement — being upfront that this is the public Telco Customer Churn dataset used as a SaaS proxy. |

## 9. Key Performance Indicators (KPIs)

- Overall churn rate (%)
- Monthly recurring revenue (MRR) at risk ($ and % of total)
- Churn rate by contract type, tenure bucket, add-on service, and payment method
- Retention rate by tenure (proxy cohort view)
- Number and value of high-priority at-risk accounts identified

## 10. User Stories

| ID | User Story |
|---|---|
| US-01 | As a Customer Success Manager, I want a list of high-risk accounts with reasons, so that I can prioritize outreach before they cancel. |
| US-02 | As a Customer Success Manager, I want a recommended retention action for each at-risk customer, so that I know what to offer without guessing. |
| US-03 | As a Revenue Leader, I want to see total MRR at risk, so that I can quantify the financial impact of churn to leadership. |
| US-04 | As a Revenue Leader, I want to see which customer segments churn most, so that I can direct retention budget where it matters most. |
| US-05 | As a Data/Analytics stakeholder, I want the churn model's predictions to be explainable, so that I can trust and validate its recommendations before acting on them. |

## 11. Success Criteria

This project will be considered successful if it:
- Clearly identifies at least 2–3 statistically meaningful churn drivers from the data
- Produces a working churn prediction model with interpretable outputs
- Produces AI-generated explanations and recommendations that are specific and grounded in the customer's actual data (not generic)
- Presents findings in a dashboard usable by a non-technical business stakeholder
- Translates findings into an estimated dollar impact (MRR saved) in the final business case

## 12. Risks

| Risk | Mitigation |
|---|---|
| Retention-by-tenure is a proxy metric, not true cohort analysis, due to missing signup dates | Document this limitation explicitly in project documentation and avoid overstating its precision |
| AI-generated explanations could hallucinate reasons not supported by the data | Ground each explanation in the model's actual feature importances for that customer, rather than open-ended generation |
| Dataset is public and widely used, reducing novelty | Differentiate through the business framing, AI recommendation layer, and business case, rather than the dataset itself |
