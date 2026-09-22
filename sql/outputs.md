- Overall churn rate: 26.54%
- MRR at total: $456,116.6 , MRR lost to churn: $139,130.85 (30.5% at risk)
- Month-to-month churn: 42.71% , One year: 11.27% , Two year: 2.83%
- 0-12 months tenure churn: 47.44% vs 49+ months: 9.51%
- No TechSupport churn: 41.64% vs Yes TechSupport: 15.17%
- Electronic check churn: 45.29% (highest payment method)


Model: Logistic Regression
Accuracy: 0.8211497515968772
Precision: 0.6861538461538461
Recall: 0.5978552278820375
Confusion Matrix: [[934 102]
 [150 223]]

Top 5 churn-driving factors: 
10     InternetService_Fiber optic     1.000622
3                     TotalCharges     0.661221
23             StreamingMovies_Yes     0.367335
26            PaperlessBilling_Yes     0.331999
28  PaymentMethod_Electronic check     0.320312

Top 5 churn-preventing factors: 
14  OnlineBackup_No internet service    -0.149900
20   StreamingTV_No internet service    -0.149900
6                     Dependents_Yes    -0.159536
19                   TechSupport_Yes    -0.319009
2                     MonthlyCharges    -0.335058