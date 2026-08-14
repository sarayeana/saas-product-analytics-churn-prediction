# Business Questions

## SaaS Product Analytics & Churn Prediction

This document defines the business questions that will guide the analysis, feature engineering, machine learning, and final recommendations of the project.

The goal is not simply to build a churn prediction model. The project aims to understand the complete customer lifecycle:

```text
Acquisition
    ↓
Signup
    ↓
Onboarding
    ↓
Product Adoption
    ↓
Engagement
    ↓
Subscription
    ↓
Retention
    ↓
Revenue
    ↓
Support Experience
    ↓
Churn Risk

```

# Business Questions

## 1. Executive-Level Questions

These questions provide the overall business perspective.

1. **Q1.** How many users and companies are using the SaaS platform?
2. **Q2.** How many users are active versus inactive?
3. **Q3.** What percentage of users are paying customers?
4. **Q4.** What is the current Monthly Recurring Revenue (MRR)?
5. **Q5.** What is the estimated Annual Recurring Revenue (ARR)?
6. **Q6.** What is the overall customer churn rate?
7. **Q7.** Which customer segments generate the most revenue?
8. **Q8.** Which customer segments have the highest churn?
9. **Q9.** What are the strongest behavioral indicators of customer retention?
10. **Q10.** Which customers should the business prioritize for retention efforts?

---

# 2. User & Customer Profile Analysis

The `users.csv` dataset will be used to understand the customer base.

11. **Q11.** What is the distribution of users by country?
12. **Q12.** What is the distribution of users by industry?
13. **Q13.** What is the distribution of users by company size?
14. **Q14.** Which acquisition channels generate the most users?
15. **Q15.** Which acquisition channels generate the most paying customers?
16. **Q16.** Which acquisition channels generate the highest-value customers?
17. **Q17.** How are customers distributed across Free, Starter, Professional, and Enterprise plans?
18. **Q18.** How does user role vary across subscription plans?
19. **Q19.** Which company sizes show the highest product engagement?
20. **Q20.** Which industries have the highest customer retention?

---

# 3. Acquisition Analysis

The project will investigate how customers enter the SaaS platform.

21. **Q21.** Which acquisition channels generate the most signups?
22. **Q22.** Which acquisition channels generate the highest percentage of paid users?
23. **Q23.** Which acquisition channels generate the highest MRR?
24. **Q24.** Which acquisition channels have the highest churn rate?
25. **Q25.** Do customers acquired through referrals have better retention than customers from paid channels?
26. **Q26.** Which acquisition channels produce the most engaged users?
27. **Q27.** Is there a relationship between acquisition channel and customer lifetime?

---

# 4. Onboarding Analysis

Successful onboarding is expected to influence product adoption and retention.

28. **Q28.** What percentage of users start onboarding?
29. **Q29.** What percentage of users complete onboarding?
30. **Q30.** What is the onboarding completion rate?
31. **Q31.** Do users who complete onboarding become more active?
32. **Q32.** Do users who complete onboarding have higher retention?
33. **Q33.** Do users who fail to complete onboarding have higher churn?
34. **Q34.** How does onboarding completion vary by plan?
35. **Q35.** How does onboarding completion vary by acquisition channel?
36. **Q36.** How does onboarding completion vary by company size?

---

# 5. Product Usage Analysis

The `events.csv` dataset provides detailed product behavior.

37. **Q37.** What are the most frequently used product features?
38. **Q38.** Which features are used by the largest number of users?
39. **Q39.** Which features are associated with highly engaged users?
40. **Q40.** How many events does the average active user generate?
41. **Q41.** What is the average number of active days per user?
42. **Q42.** How many sessions does the average user generate?
43. **Q43.** What is the average session duration?
44. **Q44.** How does product usage vary across subscription plans?
45. **Q45.** How does product usage vary across industries?
46. **Q46.** How does product usage vary across company sizes?
47. **Q47.** Which devices are most commonly used?
48. **Q48.** Does device type have a relationship with engagement?

---

# 6. Daily, Weekly & Monthly Activity

49. **Q49.** What is the Daily Active User (DAU) trend?
50. **Q50.** What is the Weekly Active User (WAU) trend?
51. **Q51.** What is the Monthly Active User (MAU) trend?
52. **Q52.** How does daily activity change over time?
53. **Q53.** Which days of the week have the highest activity?
54. **Q54.** Which hours of the day have the highest product activity?
55. **Q55.** What is the DAU/MAU ratio?
56. **Q56.** Is product engagement increasing or decreasing over time?

---

# 7. Feature Adoption Analysis

Feature adoption is a major product-health indicator.

57. **Q57.** What percentage of users adopt each major feature?
58. **Q58.** Which features have the highest adoption rate?
59. **Q59.** Which features have the lowest adoption rate?
60. **Q60.** Does feature adoption increase with subscription tier?
61. **Q61.** Do users who adopt more features have higher retention?
62. **Q62.** Is feature adoption associated with lower churn?
63. **Q63.** Which features appear to be most important for highly engaged customers?
64. **Q64.** Are there features that Enterprise customers use significantly more than Free or Starter customers?

---

# 8. Funnel Analysis

The product funnel will be analyzed using event data.

## Core Funnel

```text
Signup
   ↓
Onboarding Started
   ↓
Onboarding Completed
   ↓
Project Created
   ↓
Task Created
   ↓
Task Completed
   ↓
Team Member Invited
   ↓
Paid Subscription
```

65. **Q65.** What percentage of users enter each funnel stage?
66. **Q66.** What is the conversion rate between each funnel stage?
67. **Q67.** Where is the largest funnel drop-off?
68. **Q68.** Which customer segments have the highest funnel conversion?
69. **Q69.** Does onboarding completion improve downstream conversion?
70. **Q70.** Which acquisition channels have the strongest funnel performance?
71. **Q71.** Which subscription plans have the highest activation rate?

---

# 9. Engagement Analysis

72. **Q72.** What defines a highly engaged user?
73. **Q73.** What defines a low-engagement user?
74. **Q74.** What is the average number of events for active users?
75. **Q75.** How many active days does a typical retained customer have?
76. **Q76.** Do retained users have more sessions than churned users?
77. **Q77.** Do retained users use more product features than churned users?
78. **Q78.** Is session duration associated with retention?
79. **Q79.** How does engagement differ between Free and paid customers?
80. **Q80.** How does engagement change before churn?

---

# 10. Subscription Analysis

The `subscriptions.csv` dataset will be used to understand subscription behavior.

81. **Q81.** How many users are on each subscription plan?
82. **Q82.** What percentage of users are paying customers?
83. **Q83.** What is the distribution of monthly recurring revenue?
84. **Q84.** Which plans contribute the most MRR?
85. **Q85.** Which plans contribute the most ARR?
86. **Q86.** What is the average revenue per paying user?
87. **Q87.** What is the average subscription tenure?
88. **Q88.** How does tenure vary by subscription plan?
89. **Q89.** How many customers have upgraded?
90. **Q90.** How many customers have downgraded?
91. **Q91.** Which plans have the highest upgrade activity?
92. **Q92.** Which plans have the highest downgrade activity?

---

# 11. Revenue Analysis

93. **Q93.** What is total MRR?
94. **Q94.** What is estimated ARR?
95. **Q95.** What is Average Revenue Per User (ARPU)?
96. **Q96.** What is Average Revenue Per Paying User (ARPPU)?
97. **Q97.** Which countries generate the most revenue?
98. **Q98.** Which industries generate the most revenue?
99. **Q99.** Which company sizes generate the most revenue?
100. **Q100.** Which acquisition channels generate the most revenue?
101. **Q101.** Which subscription plans generate the highest revenue?
102. **Q102.** What percentage of revenue comes from Enterprise customers?
103. **Q103.** What percentage of revenue comes from Professional customers?

---

# 12. Retention Analysis

Retention is one of the most important SaaS metrics.

104. **Q104.** What percentage of users remain active after signup?
105. **Q105.** What is the Day-7 retention rate?
106. **Q106.** What is the Day-30 retention rate?
107. **Q107.** What is the Day-60 retention rate?
108. **Q108.** What is the Day-90 retention rate?
109. **Q109.** How does retention vary by signup cohort?
110. **Q110.** Which acquisition cohorts have the strongest retention?
111. **Q111.** Which subscription plans have the strongest retention?
112. **Q112.** How does retention differ between onboarded and non-onboarded users?
113. **Q113.** How does feature adoption affect retention?

---

# 13. Cohort Analysis

Users will be grouped into signup cohorts.

### Example

```text
January 2026 Cohort
February 2026 Cohort
March 2026 Cohort
April 2026 Cohort
...
```

114. **Q114.** Which monthly cohorts have the highest retention?
115. **Q115.** Which cohorts experience the fastest drop in activity?
116. **Q116.** Has customer retention improved over time?
117. **Q117.** Do newer cohorts behave differently from older cohorts?
118. **Q118.** Which acquisition channels produce the strongest cohorts?
119. **Q119.** Which subscription plans produce the strongest cohorts?

---

# 14. Churn Analysis

Churn is the central business problem of the project.

120. **Q120.** What is the overall customer churn rate?
121. **Q121.** What percentage of paying customers churn?
122. **Q122.** Which subscription plans have the highest churn?
123. **Q123.** Which industries have the highest churn?
124. **Q124.** Which countries have the highest churn?
125. **Q125.** Which company sizes have the highest churn?
126. **Q126.** Which acquisition channels have the highest churn?
127. **Q127.** Does onboarding completion reduce churn?
128. **Q128.** Does higher product usage reduce churn?
129. **Q129.** Does feature adoption reduce churn?
130. **Q130.** Does support-ticket volume relate to churn?
131. **Q131.** Does low customer satisfaction relate to churn?
132. **Q132.** Does longer resolution time relate to churn?
133. **Q133.** Are reopened tickets associated with churn?
134. **Q134.** Does subscription tenure affect churn?

---

# 15. Pre-Churn Behavior

A major objective is to identify behavioral patterns that occur before customers leave.

135. **Q135.** How does activity change during the months before churn?
136. **Q136.** Do churned customers show declining login frequency?
137. **Q137.** Do churned customers use fewer features before leaving?
138. **Q138.** Does session frequency decline before churn?
139. **Q139.** Does session duration decline before churn?
140. **Q140.** Does support activity increase before churn?
141. **Q141.** Does customer satisfaction decline before churn?
142. **Q142.** Are downgrades a leading indicator of churn?
143. **Q143.** Are long periods of inactivity associated with future churn?

---

# 16. Support Analysis

The `support_tickets.csv` dataset allows us to evaluate customer support quality.

144. **Q144.** How many support tickets are created?
145. **Q145.** What is the average number of tickets per user?
146. **Q146.** Which support categories generate the most tickets?
147. **Q147.** Which priority levels generate the most tickets?
148. **Q148.** Which support channels are most commonly used?
149. **Q149.** What is the average resolution time?
150. **Q150.** Which ticket categories take the longest to resolve?
151. **Q151.** Which priorities have the longest resolution times?
152. **Q152.** What percentage of tickets are reopened?
153. **Q153.** What is the average customer satisfaction score?
154. **Q154.** Which support categories have the lowest satisfaction?
155. **Q155.** Does slower resolution lead to lower satisfaction?

---

# 17. Support Experience & Churn

156. **Q156.** Do customers with more support tickets have higher churn?
157. **Q157.** Do customers with low satisfaction have higher churn?
158. **Q158.** Does a high number of unresolved tickets increase churn risk?
159. **Q159.** Are reopened tickets associated with higher churn?
160. **Q160.** Does resolution time affect churn?
161. **Q161.** Which support categories are most strongly associated with churn?
162. **Q162.** Does the relationship between support experience and churn differ by subscription plan?

---

# 18. Customer Segmentation

Customers will be segmented using behavioral and business characteristics.

### Potential Dimensions

* Engagement
* Revenue
* Product Adoption
* Tenure
* Support Experience
* Churn Risk

### Potential Segments

* Highly Engaged Customers
* Low Engagement Customers
* High-Value Customers
* At-Risk Customers
* New Customers
* Power Users
* Low-Adoption Customers
* Support-Heavy Customers

### Business Questions

163. **Q163.** Who are the highest-value customers?
164. **Q164.** Who are the most engaged customers?
165. **Q165.** Which customers are at the highest risk of churn?
166. **Q166.** Which customers have high revenue but declining engagement?
167. **Q167.** Which customers have high product usage but low subscription value?
168. **Q168.** Which customers should receive proactive retention campaigns?

---

# 19. Churn Prediction

Machine learning will be used to predict customer churn.

## Target

```text
churn = 1 → Customer churned
churn = 0 → Customer remained active
```

169. **Q169.** Can we predict which customers are likely to churn?
170. **Q170.** Which customer features provide the strongest predictive signal?
171. **Q171.** Can product engagement predict churn?
172. **Q172.** Can support experience improve churn prediction?
173. **Q173.** Can subscription information improve churn prediction?
174. **Q174.** Which machine-learning model performs best?

### Candidate Models

* Logistic Regression
* Random Forest
* XGBoost

---

# 20. Model Evaluation

Because churn prediction is a classification problem, multiple evaluation metrics will be considered.

175. **Q175.** What is the model's Precision?
176. **Q176.** What is the model's Recall?
177. **Q177.** What is the model's F1-score?
178. **Q178.** What is the ROC-AUC?
179. **Q179.** What is the PR-AUC?
180. **Q180.** Which metric should be prioritized for the business?

For customer retention, **Recall** may be particularly important because missing a genuinely at-risk customer can result in lost recurring revenue.

However, excessive false positives can also waste retention resources.

Therefore, the final threshold should consider:

```text
False Negatives
        +
False Positives
        +
Retention Cost
        +
Potential Revenue Loss
```

---

# 21. Model Explainability

The model should not only predict churn but also explain why customers are considered risky.

181. **Q181.** What are the most important churn predictors?
182. **Q182.** Does recent activity have a strong influence on churn prediction?
183. **Q183.** Does feature adoption influence churn probability?
184. **Q184.** Does support satisfaction influence churn probability?
185. **Q185.** Does subscription tenure influence churn probability?
186. **Q186.** Which characteristics increase predicted churn risk?
187. **Q187.** Which characteristics decrease predicted churn risk?

**SHAP** will be considered for model explainability.

---

# 22. Customer Risk Scoring

The final model can produce a customer-level risk score.

### Example

```text
Customer: U000123

Churn Probability: 82%

Risk Level: HIGH

Main Risk Factors:
- Low recent activity
- Low feature adoption
- 18 days since last activity
- Multiple support tickets
- Low satisfaction
```

188. **Q188.** Which customers have the highest predicted churn probability?
189. **Q189.** How many customers fall into High, Medium, and Low risk groups?
190. **Q190.** How much MRR is associated with high-risk customers?
191. **Q191.** Which high-risk customers generate the most revenue?
192. **Q192.** Which high-risk customers should be prioritized by the retention team?

---

# 23. Revenue at Risk

Churn prediction will also be connected to financial impact.

193. **Q193.** How much MRR is currently associated with high-risk customers?
194. **Q194.** What percentage of total MRR is at risk?
195. **Q195.** Which subscription plans have the greatest revenue at risk?
196. **Q196.** Which industries have the greatest revenue at risk?
197. **Q197.** Which acquisition channels have the greatest revenue at risk?
198. **Q198.** Which individual customers represent the largest potential revenue loss?

---

# 24. Business Recommendations

The final analysis should answer:

199. **Q199.** How can the company improve onboarding?
200. **Q200.** Which product features should receive more attention?
201. **Q201.** Which customer segments need proactive engagement?
202. **Q202.** How can customer support reduce churn?
203. **Q203.** Which acquisition channels should receive more investment?
204. **Q204.** Which customers should receive retention offers?
205. **Q205.** Which customers should receive product education?
206. **Q206.** Which customers should receive customer-success intervention?
207. **Q207.** How can the company reduce revenue at risk?

---

# 25. Final Executive Questions

The final project should be able to answer the following questions clearly:

* Who are our customers?
* How are they using the product?
* Which features drive engagement?
* Where do users drop out of the funnel?
* Which customers stay and which customers leave?
* Why do customers churn?
* How does support experience affect retention?
* Which customers generate the most revenue?
* Which customers are most likely to churn?
* How much revenue is at risk?
* What actions should the business take?

---

# 26. Analytical Roadmap

The business questions will be answered in the following sequence:

```text
01. Data Understanding
        ↓
02. Data Quality & Validation
        ↓
03. User & Customer Analysis
        ↓
04. Product Usage Analysis
        ↓
05. Engagement Analysis
        ↓
06. Funnel Analysis
        ↓
07. Retention & Cohort Analysis
        ↓
08. Revenue & Subscription Analysis
        ↓
09. Support Analysis
        ↓
10. Churn Analysis
        ↓
11. Feature Engineering
        ↓
12. Churn Prediction
        ↓
13. Model Evaluation
        ↓
14. Model Explainability
        ↓
15. Customer Risk Scoring
        ↓
16. Revenue-at-Risk Analysis
        ↓
17. Streamlit Dashboard
        ↓
18. Business Recommendations
```

---

# 27. Expected Final Deliverables

The completed project should produce the following outputs.

## Data Analysis

* Product usage metrics
* Engagement metrics
* Funnel metrics
* Retention metrics
* Cohort analysis
* Revenue metrics
* Support metrics
* Churn analysis

## Machine Learning

* User-level churn features
* Baseline model
* Logistic Regression
* Random Forest
* XGBoost
* Model comparison
* Model evaluation
* Feature importance
* SHAP explainability
* Churn probability
* Customer risk score

## Business Outputs

* High-risk customer list
* Revenue at risk
* Churn drivers
* Retention recommendations
* Product recommendations
* Support recommendations

---

# Application

A **Streamlit dashboard** will bring the analytical results together.

### Dashboard Structure

```text
Executive Overview
        ↓
Product Analytics
        ↓
Funnel
        ↓
Retention
        ↓
Revenue
        ↓
Support
        ↓
Churn
        ↓
Customer Risk
```

The application should allow users to explore business performance, customer behavior, churn risk, and revenue exposure interactively.

---

# 28. Success Criteria

The project will be considered successful if it can:

* Explain how customers use the SaaS product.
* Identify important engagement patterns.
* Measure product adoption and retention.
* Identify major funnel drop-offs.
* Measure recurring revenue.
* Identify important churn patterns.
* Quantify the relationship between support experience and churn.
* Predict customer churn with a meaningful evaluation framework.
* Explain individual churn predictions.
* Identify high-value customers at risk.
* Quantify revenue at risk.
* Translate analytical findings into actionable business recommendations.

---

# Project Objective

The overall objective of this project is:

> **To use SaaS product usage, subscription, and customer support data to understand customer behavior, identify the drivers of retention and churn, predict customers at risk of leaving, quantify revenue at risk, and provide actionable recommendations for improving customer retention and business growth.**

---

# Related Documentation

| Document                | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| `README.md`             | Project overview and setup                  |
| `data_dictionary.md`    | Dataset and column definitions              |
| `data_model.md`         | Dataset relationships and analytical model  |
| `business_questions.md` | Business questions and analytical roadmap   |
| `methodology.md`        | Analytical and machine-learning methodology |
| `insights.md`           | Final business insights and recommendations |
