# Methodology

## 1. Project Overview

This project analyzes SaaS product usage, customer behavior, subscriptions, revenue, and churn to identify important business patterns and generate actionable insights.

The project follows an end-to-end analytics workflow:

```text
Raw Data
   ↓
Data Validation
   ↓
Data Cleaning
   ↓
Data Preparation
   ↓
Exploratory Data Analysis
   ↓
Business Metrics
   ↓
Customer / Product Analysis
   ↓
Analytics CSV Generation
   ↓
Streamlit Dashboard
   ↓
Business Insights
```

The methodology is designed to keep data processing, analysis, and dashboard presentation separated.

---

# 2. Business Objective

The main objective is to understand how customers use the SaaS product and how their behavior relates to subscription activity, revenue, and churn.

The analysis focuses on questions such as:

* How large is the user base?
* How active are users?
* How many users are paying customers?
* How much recurring revenue does the business generate?
* Which subscription plans generate the most revenue?
* How does customer activity vary across segments?
* What patterns are associated with customer churn?
* How does product usage relate to customer retention?
* What business areas require attention?

---

# 3. Data Sources

The project uses multiple datasets representing different parts of the SaaS business.

The main data domains include:

* Users
* Product events
* Subscriptions
* Support tickets

These datasets represent different aspects of the customer lifecycle.

```text
Users
  ├── Customer information
  │
  ├── Events
  │      └── Product usage
  │
  ├── Subscriptions
  │      └── Plans / revenue / status
  │
  └── Support Tickets
         └── Customer support activity
```

---

# 4. Data Validation

Before performing analysis, the datasets are validated.

The validation process checks for:

* Dataset structure
* Column names
* Data types
* Missing values
* Duplicate records
* Invalid values
* Unexpected categories
* Date consistency
* Key fields required for analysis

The objective is to identify data-quality problems before they affect analytical results.

---

# 5. Data Cleaning

The raw datasets are cleaned before analysis.

Typical cleaning operations include:

### Missing Values

Missing values are investigated based on the meaning of each field.

Depending on the column, missing values may be:

* Replaced
* Retained
* Excluded
* Treated as an unknown category

The treatment depends on the business meaning of the field.

### Duplicate Records

Duplicate records are checked to prevent double-counting users, events, subscriptions, or support tickets.

### Data Types

Columns are converted into appropriate data types.

Examples include:

```text
Date → datetime
Revenue → numeric
User ID → identifier
Subscription status → categorical
```

---

# 6. Date Preparation

Date fields are standardized so that time-based analysis can be performed consistently.

Date information can be used to generate analytical dimensions such as:

* Year
* Month
* Week
* Day
* Month-Year

These fields support trend analysis and time-based business metrics.

---

# 7. Data Preparation

After cleaning, the datasets are transformed into analysis-ready structures.

The preparation process includes:

* Standardizing column names
* Converting data types
* Creating derived fields
* Preparing categorical fields
* Creating analytical metrics
* Preparing datasets for aggregation

The objective is to produce reliable datasets that can be reused across multiple analyses.

---

# 8. Exploratory Data Analysis

Exploratory Data Analysis is performed to understand the structure and behavior of the data.

The analysis examines:

* Dataset dimensions
* Variable distributions
* Customer behavior
* Product usage
* Subscription patterns
* Revenue patterns
* Churn patterns
* Support activity

EDA helps identify important patterns before building the final business analysis.

---

# 9. User Analysis

User-level analysis examines the SaaS customer base.

Important metrics include:

* Total users
* Active users
* Inactive users
* Paying customers
* Customer distribution
* Customer activity

This analysis establishes the overall health of the user base.

---

# 10. Product Usage Analysis

Product events are analyzed to understand customer engagement.

The analysis considers:

* Number of events
* User activity
* Feature usage
* Usage frequency
* Engagement patterns
* Activity differences between customer groups

The goal is to determine how customers interact with the product.

---

# 11. Subscription Analysis

Subscription data is analyzed to understand customer plans and subscription behavior.

The analysis includes:

* Subscription status
* Subscription plans
* Active subscriptions
* Cancelled subscriptions
* Subscription duration
* Revenue contribution

This helps identify which plans are most important to the business.

---

# 12. Revenue Analysis

Revenue analysis focuses on recurring SaaS revenue.

Key metrics include:

### Monthly Recurring Revenue

MRR represents recurring monthly subscription revenue.

```text
MRR = Sum of active recurring subscription revenue
```

### Annual Recurring Revenue

ARR provides an annualized view of recurring revenue.

```text
ARR = MRR × 12
```

### Average Revenue

Average revenue metrics help compare customer or subscription performance.

Revenue is also analyzed across:

* Subscription plans
* Customer segments
* Time periods
* Customer groups

---

# 13. Churn Analysis

Churn analysis identifies customers who discontinue their subscriptions or become inactive according to the project's churn definition.

The analysis examines:

* Overall churn
* Churn over time
* Churn by subscription plan
* Churn by customer segment
* Churn by customer activity
* Behavioral differences between retained and churned customers

The purpose is not only to measure churn but also to identify potential behavioral patterns associated with customer loss.

---

# 14. Customer Segmentation

Customers can be grouped according to relevant behavioral or business characteristics.

Possible segmentation dimensions include:

* Revenue contribution
* Product engagement
* Subscription plan
* Activity level
* Customer status

Segmentation allows the business to compare different customer groups instead of treating the entire customer base as one population.

---

# 15. Support Analysis

Support-ticket data is analyzed to understand customer service activity.

The analysis considers:

* Ticket volume
* Ticket categories
* Ticket priority
* Resolution activity
* Support behavior by customer group

Support activity can provide additional context when evaluating customer satisfaction and churn.

---

# 16. Business KPI Calculation

The cleaned and prepared data is used to calculate the project's major business KPIs.

Examples include:

```text
Total Users
Active Users
Paying Customers
MRR
ARR
Average Revenue
Churn Rate
Subscription Count
Product Usage
Support Ticket Volume
```

These KPIs form the foundation of the executive dashboard.

---

# 17. Analytics Dataset Generation

After the major analyses are completed, the results are saved as analytics CSV files.

The general workflow is:

```text
Cleaned Data
     ↓
Analysis
     ↓
Aggregations
     ↓
Business Metrics
     ↓
Analytics CSV
```

This approach allows the Streamlit application to consume prepared analytical results rather than repeatedly performing all analytical calculations during dashboard execution.

---

# 18. Streamlit Dashboard

The final analytics CSV files are used by the Streamlit application.

The dashboard provides:

* KPI cards
* Interactive charts
* Business performance analysis
* Customer analysis
* Revenue analysis
* Churn analysis
* Product usage analysis
* Other analytical views

The application acts as the presentation layer of the project.

---

# 19. Quality Control

Before finalizing the dashboard, the following checks are performed:

* Data files exist
* Required columns exist
* Data types are appropriate
* Analytics CSVs contain data
* Calculated metrics are reasonable
* Dashboard loads successfully
* Charts render correctly
* Filters work as expected
* No unnecessary transformations are introduced

If a chart references a column that does not exist, the chart should be corrected against the actual generated analytics CSV schema rather than assuming a column name.

---

# 20. Business Interpretation

The final stage converts analytical results into business insights.

The interpretation focuses on:

```text
What happened?
      ↓
Why might it be happening?
      ↓
Which customers / products / plans are affected?
      ↓
Why does it matter?
      ↓
What should the business do?
```

This ensures that the project goes beyond descriptive statistics and produces practical business recommendations.

---

# 21. Final Methodology

The complete methodology can therefore be summarized as:

```text
1. Collect SaaS Data
        ↓
2. Validate Data
        ↓
3. Clean Data
        ↓
4. Prepare Data
        ↓
5. Perform EDA
        ↓
6. Calculate Business Metrics
        ↓
7. Analyze Users
        ↓
8. Analyze Product Usage
        ↓
9. Analyze Subscriptions
        ↓
10. Analyze Revenue
        ↓
11. Analyze Churn
        ↓
12. Analyze Support Activity
        ↓
13. Generate Analytics CSVs
        ↓
14. Build Streamlit Dashboard
        ↓
15. Interpret Business Findings
        ↓
16. Provide Recommendations
```

This methodology provides a structured and reproducible approach for SaaS product analytics and churn analysis.
