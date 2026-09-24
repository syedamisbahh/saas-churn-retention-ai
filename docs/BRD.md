# Business Requirements Document (BRD)
## SaaS Churn Prediction & AI-Driven Retention System

**Document version:** 1.4
**Author:** Syeda Misbah Hussain
**Date:** 09/24/2026
**Status:** Draft

## Revision History

| Version | Date | Change |
|---|---|---|
| 1.0 | 09/17/2026 | Initial draft — business problem, objectives, scope, and requirements defined |
| 1.1 | 09/22/2026 | Confirmed FR-04, FR-05, and NFR-01 against the churn prediction model actually built (logistic regression, standardized numeric features, 80/20 train/test split). Added the model's recall limitation to the Risks table. |
| 1.2 | 09/23/2026 | Confirmed FR-06 and FR-07 as implemented, with the AI explanation/recommendation layer built using the Groq API (openai/gpt-oss-20b). Added a risk noting manual review of AI output does not scale. |
| 1.3 | 09/23/2026 | Documented end-to-end pipeline sequence and added the process flow diagram (before/after workflow) to project documentation. Added a constraint and risk noting the pipeline is not yet fully automated. |
| 1.4 | 09/24/2026 | Added FR-11 confirming the business case as implemented, with real scenario-based MRR-saved estimates. Added a risk noting the business case is an estimate, not a measured outcome, and a risk noting the AI layer currently covers only 10 of 519 flagged customers. |

---

## 1. Business Problem

SaaS companies lose recurring revenue when at-risk customers churn without warning. Support and Customer Success teams typically identify churn risk reactively - after a customer has already cancelled or stopped engaging - because manual account monitoring cannot scale with the volume of active customers. This results in preventable revenue loss and missed opportunities for timely retention intervention.

## 2. Business Objective

Build a system that proactively identifies at-risk customers, quantifies the revenue impact of churn, and recommends specific, actionable retention steps - before a customer cancels, rather than after.

## 3. Scope

### In Scope
- Analysis of historical customer data to identify churn drivers
- Quantification of churn rate and monthly recurring revenue (MRR) at risk
- A predictive model to flag active customers likely to churn
- An AI-generated layer that explains each at-risk customer's risk factors and recommends a retention action, in plain business language
- A dashboard presenting churn KPIs, segmentation, and at-risk customers to a non-technical business stakeholder
- A process flow diagram illustrating the shift from manual to AI-assisted retention workflow
- A business case translating model findings into an estimated dollar impact

### Out of Scope
- Live integration with a production billing or CRM system
- Automated execution of retention actions (e.g., auto-sending discount offers)
- Real-time (streaming) data processing
- A/B testing of retention strategies
- Full pipeline orchestration (the current pipeline runs as sequential standalone scripts, not a single automated job)
- Scaling the AI recommendation layer beyond the top 10 highest-risk customers

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
- Retention success rates used in the business case (10%/20%/30%) are illustrative assumptions, not derived from a historical A/B test or real campaign data.

## 6. Constraints

- No signup/join date is available in the dataset, so true cohort-based retention analysis (tracking a specific monthly cohort over time) is not possible. Tenure-based retention is used as a proxy instead.
- The predictive model must remain interpretable (e.g., logistic regression or decision tree) rather than a high-complexity black-box model, so that its outputs can be explained in plain language to a business stakeholder.
- Numeric features used by the model (tenure, monthly charges, total charges) are correlated with one another, which can make individual model coefficients less stable to interpret in isolation, even though overall model performance remains valid.
- The current pipeline (data cleaning → modeling → AI recommendation generation) runs as separate scripts executed in sequence, not a single automated or scheduled job; SQL-based analysis in particular still requires manual execution.

## 7. Functional Requirements

| ID | Requirement | Status |
|---|---|---|
| FR-01 | The system shall calculate the overall customer churn rate. | Implemented |
| FR-02 | The system shall calculate monthly recurring revenue (MRR) and the portion of MRR attributable to churned customers. | Implemented |
| FR-03 | The system shall segment churn rate by contract type, tenure, add-on services, and payment method. | Implemented |
| FR-04 | The system shall predict a churn probability score for each active customer. | Implemented — logistic regression model, evaluated on held-out test data |
| FR-05 | The system shall identify the top factors contributing to each customer's predicted churn risk. | Implemented — model coefficients extracted and cross-checked against SQL segmentation findings |
| FR-06 | The system shall generate a plain-English explanation of each at-risk customer's risk factors, using an AI language model. | Implemented — Groq API (openai/gpt-oss-20b), applied to the top 10 highest-risk active customers |
| FR-07 | The system shall generate a recommended retention action for each at-risk customer, using an AI language model. | Implemented — one specific action generated per customer, alongside the explanation |
| FR-08 | The system shall present churn KPIs, segmentation breakdowns, and at-risk customers in an interactive dashboard. | Implemented |
| FR-09 | The dashboard shall allow filtering of results by at least one dimension (e.g., contract type). | Implemented |
| FR-10 | The system's end-to-end workflow shall be documented with a process flow diagram illustrating the shift from manual to AI-assisted retention. | Implemented — before/after process flow diagram, `docs/process_flow.png` |
| FR-11 | The system shall translate model findings into an estimated dollar impact (business case). | Implemented — 519 active customers flagged above 50% churn risk, representing $41,254.65 in monthly recurring revenue; scenario-based estimates calculated at 10%/20%/30% retention success rates |

## 8. Non-Functional Requirements

| ID | Requirement | Source |
|---|---|---|
| NFR-01 | The churn prediction model shall be interpretable (e.g., logistic regression or decision tree), with feature importances or coefficients available for explanation. | Directly discussed: an interpretable model is required so the AI explanation layer can explain *why* a customer was flagged, rather than working against a black box. Confirmed against the actual model built: a logistic regression model with extracted, ranked coefficients. |
| NFR-02 | Dashboard visuals shall be understandable by a non-technical business stakeholder (e.g., a Customer Success Manager) without requiring knowledge of the underlying SQL or data model. | Directly discussed: the dashboard's stated purpose throughout was to be usable by a business stakeholder, not just a technical audience — this was the reasoning behind every chart-type decision (Chart Selection Rationale). |
| NFR-03 | AI-generated explanations and retention recommendations shall be grounded in the model's actual feature importances or the customer's real data fields, and shall not fabricate reasons unsupported by the data. | Directly discussed and confirmed: the prompt explicitly constrains the model to the customer's real data fields, and all 10 generated outputs were manually cross-checked against the database before acceptance. |
| NFR-04 | Customer data used in this project shall come only from a public, non-sensitive dataset; no real customer PII shall be used. | Directly discussed: the dataset disclosure and honesty requirement — being upfront that this is the public Telco Customer Churn dataset used as a SaaS proxy. |
| NFR-05 | Any estimated financial impact presented in the business case shall be clearly labeled as a scenario-based estimate, not a guaranteed or measured outcome. | Directly discussed and confirmed: the business case explicitly presents three retention-rate scenarios (10%/20%/30%) and states the figures illustrate order of magnitude, not a committed projection. |

## 9. Key Performance Indicators (KPIs)

- Overall churn rate (%)
- Monthly recurring revenue (MRR) at risk ($ and % of total)
- Churn rate by contract type, tenure bucket, add-on service, payment method, and internet service type
- Retention rate by tenure (proxy cohort view)
- Number and value of high-priority at-risk accounts identified
- Model performance: accuracy, precision, and recall on held-out test data
- Estimated MRR saved under 10%/20%/30% retention scenarios

## 10. User Stories

| ID | User Story |
|---|---|
| US-01 | As a Customer Success Manager, I want a list of high-risk accounts with reasons, so that I can prioritize outreach before they cancel. |
| US-02 | As a Customer Success Manager, I want a recommended retention action for each at-risk customer, so that I know what to offer without guessing. |
| US-03 | As a Revenue Leader, I want to see total MRR at risk, so that I can quantify the financial impact of churn to leadership. |
| US-04 | As a Revenue Leader, I want to see which customer segments churn most, so that I can direct retention budget where it matters most. |
| US-05 | As a Data/Analytics stakeholder, I want the churn model's predictions to be explainable, so that I can trust and validate its recommendations before acting on them. |
| US-06 | As a new stakeholder unfamiliar with the project, I want a visual illustration of how the workflow changes with this system, so that I can quickly understand its value without reading technical documentation. |
| US-07 | As a Revenue Leader, I want a realistic estimate of potential MRR savings under different retention success scenarios, so that I can gauge the potential value of investing in this system. |

## 11. Success Criteria

This project is considered successful, as confirmed against the delivered system:
- Clearly identifies at least 2–3 statistically meaningful churn drivers from the data (contract type, tenure, internet service type, add-on services all confirmed via SQL and model coefficients)
- Produces a working churn prediction model with interpretable outputs (logistic regression, 82.1% accuracy, ranked coefficients)
- Produces AI-generated explanations and recommendations that are specific and grounded in the customer's actual data (10 customers, manually validated against source records)
- Presents findings in a dashboard usable by a non-technical business stakeholder (Tableau Public dashboard, chart choices justified by relationship type)
- Translates findings into an estimated dollar impact in the final business case (519 at-risk customers, $41,254.65 MRR, scenario-based annual impact of $49,505.58–$148,516.74)

## 12. Risks

| Risk | Mitigation |
|---|---|
| Retention-by-tenure is a proxy metric, not true cohort analysis, due to missing signup dates | Document this limitation explicitly in project documentation and avoid overstating its precision |
| AI-generated explanations could hallucinate reasons not supported by the data | Ground each explanation in the model's actual feature importances for that customer, rather than open-ended generation |
| Dataset is public and widely used, reducing novelty | Differentiate through the business framing, AI recommendation layer, and business case, rather than the dataset itself |
| The churn model, as trained, misses roughly 40% of customers who actually churn (recall of 59.8% on held-out test data) | Document this trade-off explicitly; a production deployment prioritizing recall over precision could lower the model's decision threshold, at the cost of more false alarms |
| Manual review of AI-generated output does not scale beyond a small sample (10 customers) | For a larger customer base, an automated validation step (e.g., programmatically checking that cited figures match the source record) would be needed before trusting AI output at scale |
| The pipeline is not fully automated — scripts run sequentially and manually, and SQL analysis is not yet callable from a script | Document this as a known limitation; a production version would use a scheduler or orchestration tool to run the pipeline end to end without manual steps |
| The business case relies on assumed retention success rates (10%/20%/30%) rather than measured outcomes from a real retention campaign | Clearly label all figures as scenario-based estimates; avoid presenting any single number as a guaranteed financial outcome |
| The AI recommendation layer currently covers only 10 of the 519 customers flagged as at-risk, not the full population | Document this as a proof-of-concept scope; note that scaling to the full population is a straightforward extension of the existing script, not a redesign |