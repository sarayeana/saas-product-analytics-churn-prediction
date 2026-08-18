# SaaS Product Analytics & Churn Prediction

> End-to-end Python project for analyzing SaaS product usage, customer engagement, subscription revenue, support experience, retention, and customer churn — with machine learning-based churn prediction and customer risk scoring.

---

## Project Overview

SaaS companies need to understand not only **how much revenue they generate**, but also **how customers use their product, what keeps them engaged, and why they eventually leave**.

This project simulates a real-world SaaS analytics environment by combining four interconnected datasets:

- User profiles
- Product usage events
- Subscription information
- Customer support tickets

The project uses these datasets to build a complete analytical pipeline:

```text
Raw SaaS Data
      ↓
Data Validation
      ↓
Exploratory Data Analysis
      ↓
Product Analytics
      ↓
Customer Engagement
      ↓
Funnel Analysis
      ↓
Retention & Cohort Analysis
      ↓
Revenue Analytics
      ↓
Support Analytics
      ↓
Churn Analysis
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Churn Prediction
      ↓
Customer Risk Scoring
      ↓
Revenue at Risk
      ↓
Business Recommendations
      ↓
Streamlit Dashboard

```

# 1. Business Problem

A SaaS company wants to answer several important questions:

* How are customers using the product?
* Which features are most important?
* Which users are highly engaged?
* Where do users drop out of the onboarding funnel?
* Which customers are likely to churn?
* What behaviors are associated with churn?
* Does customer support experience influence churn?
* Which customers generate the most recurring revenue?
* How much revenue is at risk?
* Which customers should the retention team prioritize?

### Objective

The objective is to transform raw SaaS activity data into **actionable business intelligence and predictive insights**.

---

# 2. Project Objectives

The project has six major objectives.

## 2.1 Product Analytics

Understand how users interact with the SaaS product.

### Key Areas

* Event activity
* Sessions
* Active users
* Feature adoption
* Product engagement
* Device usage
* User behavior

---

## 2.2 Customer Analytics

Understand who the customers are.

Analyze:

* Country
* Industry
* Company size
* User role
* Subscription plan
* Acquisition channel
* Customer tenure

---

## 2.3 Retention Analysis

Measure customer retention using:

* Cohort analysis
* Day-7 retention
* Day-30 retention
* Day-60 retention
* Day-90 retention
* Activity trends
* Engagement patterns

---

## 2.4 Revenue Analytics

Analyze SaaS subscription economics.

### Key Metrics

* MRR
* ARR
* ARPU
* ARPPU
* Revenue by plan
* Revenue by industry
* Revenue by country
* Revenue by acquisition channel

---

## 2.5 Churn Analysis

Identify factors associated with customer churn.

### Potential Churn Drivers

* Low product usage
* Low feature adoption
* Inactivity
* Poor onboarding
* Subscription downgrades
* High support volume
* Poor customer satisfaction
* Long ticket resolution times

---

## 2.6 Churn Prediction

Build machine-learning models that estimate the probability that a customer will churn.

The final system will produce:

```text
Customer
    ↓
Churn Probability
    ↓
Risk Level
    ↓
Key Risk Factors
    ↓
Recommended Action
```

---

# 3. Dataset Overview

The project contains four synthetic datasets.

| Dataset               | Approx. Rows | Grain                      | Primary Key       |
| --------------------- | -----------: | -------------------------- | ----------------- |
| `users.csv`           |       30,000 | One row per user           | `user_id`         |
| `events.csv`          |       1.55M+ | One row per product event  | `event_id`        |
| `subscriptions.csv`   |       30,000 | One row per subscription   | `subscription_id` |
| `support_tickets.csv` |        9,976 | One row per support ticket | `ticket_id`       |

> **Note:** Row counts may change if the synthetic data-generation process is regenerated.

---

# 4. Dataset Description

## 4.1 Users

Contains customer profile information.

### Important Fields

* `user_id`
* `company_id`
* `signup_date`
* `country`
* `industry`
* `company_size`
* `acquisition_channel`
* `plan`
* `role`
* `primary_device`
* `engagement_propensity`
* `onboarding_completed`

---

## 4.2 Events

Contains product usage activity.

### Important Fields

* `event_id`
* `user_id`
* `company_id`
* `event_timestamp`
* `event_type`
* `feature`
* `session_id`
* `device`
* `session_duration_minutes`

### Example Events

* `login`
* `onboarding_started`
* `onboarding_completed`
* `project_created`
* `task_created`
* `task_completed`
* `file_uploaded`
* `comment_added`
* `team_member_invited`
* `report_generated`
* `subscription_started`
* `subscription_upgraded`
* `subscription_downgraded`
* `support_viewed`

---

## 4.3 Subscriptions

Contains subscription and revenue information.

### Important Fields

* `subscription_id`
* `user_id`
* `company_id`
* `plan`
* `subscription_start_date`
* `subscription_end_date`
* `billing_frequency`
* `monthly_recurring_revenue`
* `annual_contract_value`
* `trial`
* `status`
* `acquisition_source`
* `upgrade_count`
* `downgrade_count`
* `tenure_days`

---

## 4.4 Support Tickets

Contains customer support interactions.

### Important Fields

* `ticket_id`
* `user_id`
* `company_id`
* `created_at`
* `category`
* `priority`
* `channel`
* `status`
* `resolved_at`
* `resolution_time_hours`
* `reopened`
* `satisfaction_score`
* `plan_at_ticket`
* `subscription_status_at_ticket`

---

# 5. Data Relationships

The central entity is the **user**.

```text
                         ┌─────────────────┐
                         │      USERS      │
                         │   30,000 rows   │
                         │                 │
                         │ PK: user_id     │
                         └────────┬────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
   ┌─────────────────┐  ┌─────────────────┐  ┌────────────────────┐
   │     EVENTS      │  │  SUBSCRIPTIONS  │  │  SUPPORT TICKETS   │
   │   1.55M+ rows   │  │   30,000 rows   │  │    9,976 rows      │
   │                 │  │                 │  │                    │
   │ PK: event_id    │  │ PK: sub_id      │  │ PK: ticket_id      │
   │ FK: user_id     │  │ FK: user_id     │  │ FK: user_id        │
   │ FK: company_id  │  │ FK: company_id  │  │ FK: company_id     │
   └─────────────────┘  └─────────────────┘  └────────────────────┘
```

Detailed data-model documentation is available in:

`data_model.md`

---

# 6. Key Business Metrics

The project will calculate SaaS and product analytics metrics.

## Product Metrics

| Metric           | Description                            |
| ---------------- | -------------------------------------- |
| DAU              | Daily Active Users                     |
| WAU              | Weekly Active Users                    |
| MAU              | Monthly Active Users                   |
| DAU/MAU          | User engagement ratio                  |
| Sessions         | Number of user sessions                |
| Active Days      | Number of days a user is active        |
| Feature Adoption | Percentage of users adopting a feature |

## Revenue Metrics

| Metric          | Description                                 |
| --------------- | ------------------------------------------- |
| MRR             | Monthly Recurring Revenue                   |
| ARR             | Annual Recurring Revenue                    |
| ARPU            | Average Revenue Per User                    |
| ARPPU           | Average Revenue Per Paying User             |
| Revenue at Risk | Revenue associated with high-risk customers |

## Customer Metrics

| Metric            | Description                              |
| ----------------- | ---------------------------------------- |
| Churn Rate        | Percentage of customers who churn        |
| Retention Rate    | Percentage of customers remaining active |
| Customer Tenure   | Duration of customer relationship        |
| Support Tickets   | Number of support interactions           |
| Satisfaction      | Average customer satisfaction            |
| Churn Probability | Model-estimated probability of churn     |

---

# 7. Machine Learning Problem

## Problem Type

**Binary Classification**

The model predicts:

```text
churn = 1
```

or:

```text
churn = 0
```

Where:

```text
1 = Churned
0 = Active
```

---

# 8. Feature Engineering

The raw datasets will be transformed into a **user-level analytical dataset**.

## Engagement Features

* `total_events`
* `active_days`
* `session_count`
* `avg_session_duration`
* `days_since_last_activity`
* `events_last_7_days`
* `events_last_30_days`

## Feature Adoption

* `features_used`
* `feature_adoption_rate`
* `projects_created`
* `tasks_created`
* `tasks_completed`
* `files_uploaded`
* `reports_generated`

## Subscription Features

* `monthly_recurring_revenue`
* `annual_contract_value`
* `subscription_tenure`
* `upgrade_count`
* `downgrade_count`

## Support Features

* `ticket_count`
* `avg_resolution_time`
* `avg_satisfaction`
* `reopened_ticket_count`
* `high_priority_ticket_count`

## Customer Profile Features

* `plan`
* `country`
* `industry`
* `company_size`
* `acquisition_channel`
* `role`
* `primary_device`
* `onboarding_completed`

---

# 9. Data Leakage Prevention

A major objective is to make the churn model realistic.

Only information available **before the prediction point** should be used to predict future churn.

### Do Not Use

* Post-churn events
* Future activity
* Future support tickets
* Future revenue
* Information created after churn

### Modeling Timeline

```text
Historical Customer Behavior
          ↓
Feature Engineering
          ↓
Prediction Point
          ↓
Future Churn
```

This is important because a model that uses future information may produce artificially high performance while failing in real-world deployment.

---

# 10. Machine Learning Models

The project will compare multiple classification algorithms.

## Baseline

### Logistic Regression

Used as an interpretable baseline model.

## Tree-Based Models

### Random Forest

Used to capture nonlinear relationships and feature interactions.

### XGBoost

Used as the primary advanced boosting model.

XGBoost is expected to perform well on structured customer-level tabular data.

---

# 11. Model Evaluation

The models will be evaluated using multiple metrics:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC
* PR-AUC
* Confusion Matrix

Because customer churn is a business-risk problem, particular attention will be paid to:

* Recall
* F1-Score
* ROC-AUC
* PR-AUC

The final model should balance:

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

# 12. Model Explainability

The project will use feature importance and SHAP-based analysis to explain model predictions.

### Key Question

> **Why does the model think this customer is likely to churn?**

### Example

```text
Customer: U000123

Churn Probability: 82%

Risk Level: HIGH

Risk Factors:

1. Low recent activity
2. Low feature adoption
3. Long inactivity period
4. Multiple support tickets
5. Low satisfaction score
```

---

# 13. Customer Risk Scoring

Customers will be categorized into risk levels.

```text
┌──────────────────────────────┐
│       CUSTOMER RISK          │
├──────────────────────────────┤
│                              │
│  LOW       0% - 30%          │
│  MEDIUM   30% - 60%          │
│  HIGH     60% - 80%          │
│  CRITICAL 80% - 100%         │
│                              │
└──────────────────────────────┘
```

> The exact thresholds will be determined after model calibration and business evaluation.

---

# 14. Revenue at Risk

One of the most important outputs is connecting churn probability with revenue.

### Example

```text
Customer A
MRR = $499
Churn Probability = 85%
```

### Potential Revenue at Risk

```text
Revenue at Risk
= Customer MRR × Churn Probability

= $499 × 85%

= $424.15
```

### Portfolio-Level Calculation

```text
Revenue at Risk
=
Σ(Customer MRR × Churn Probability)
```

This allows the business to prioritize customers based not only on churn probability but also on **financial impact**.

---

# 15. Project Architecture

```text
                         ┌───────────────────────┐
                         │       Raw Data        │
                         │                       │
                         │ users.csv             │
                         │ events.csv            │
                         │ subscriptions.csv     │
                         │ support_tickets.csv   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    Data Validation    │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Data Transformation │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Feature Engineering │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Product Analytics│             │ Machine Learning │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   ▼                                ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Business Insights│             │ Churn Prediction │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   └────────────────┬───────────────┘
                                    ▼
                         ┌───────────────────────┐
                         │  Customer Risk Score  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Streamlit Application │
                         └───────────────────────┘
```

---

# 16. Repository Structure

```text
saas-product-analytics-churn-prediction/
│
├── .venv/
│
├── data/
│   ├── raw/
│   │   ├── users.csv
│   │   ├── events.csv
│   │   ├── subscriptions.csv
│   │   └── support_tickets.csv
│   │
│   └── processed/
│
├── notebooks/
│   ├── 01_data_quality.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_product_analytics.ipynb
│   ├── 04_funnel_analysis.ipynb
│   ├── 05_retention_cohort_analysis.ipynb
│   ├── 06_revenue_analysis.ipynb
│   ├── 07_support_analysis.ipynb
│   ├── 08_churn_analysis.ipynb
│   ├── 09_feature_engineering.ipynb
│   ├── 10_model_training.ipynb
│   ├── 11_model_evaluation.ipynb
│   └── 12_model_explainability.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── product_analytics.py
│   ├── retention.py
│   ├── revenue.py
│   ├── churn_analysis.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── utils.py
│
├── app/
│   ├── app.py
│   ├── components.py
│   └── pages/
│
├── models/
│
├── reports/
│   ├── figures/
│   └── tables/
│
├── config/
│   └── config.yaml
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_validation.py
│   └── test_features.py
│
├── data_dictionary.md
├── data_model.md
├── business_questions.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 17. Python Project Structure

The project will follow a modular Python architecture.

## Data Layer

Responsible for:

* Loading datasets
* Validating data
* Handling missing values
* Data type conversion

### Main Files

* `data_loader.py`
* `data_validation.py`
* `preprocessing.py`

---

## Analytics Layer

Responsible for:

* Product metrics
* Engagement
* Retention
* Revenue
* Support
* Churn analysis

### Main Files

* `product_analytics.py`
* `retention.py`
* `revenue.py`
* `churn_analysis.py`

---

## Machine Learning Layer

Responsible for:

* Feature engineering
* Model training
* Model evaluation
* Prediction
* Explainability

### Main Files

* `feature_engineering.py`
* `train.py`
* `evaluate.py`
* `predict.py`

---

## Application Layer

The Streamlit application will provide an interactive interface for business users.

---

# 18. Streamlit Dashboard

The final application will contain multiple sections.

## Executive Overview

Displays:

* Total Users
* Active Users
* Paying Customers
* MRR
* ARR
* Churn Rate
* Revenue at Risk

---

## Product Analytics

Displays:

* DAU
* WAU
* MAU
* Feature adoption
* Event trends
* Session behavior

---

## Funnel

```text
Signup
  ↓
Onboarding
  ↓
Activation
  ↓
Product Usage
  ↓
Subscription
```

---

## Retention

Displays:

* Cohort retention
* Day-7 retention
* Day-30 retention
* Day-60 retention
* Day-90 retention

---

## Revenue

Displays:

* MRR
* ARR
* ARPU
* Revenue by plan
* Revenue by industry
* Revenue by country

---

## Support

Displays:

* Ticket volume
* Resolution time
* Satisfaction
* Reopened tickets
* Support categories

---

## Churn

Displays:

* Overall churn rate
* Churn by plan
* Churn by industry
* Churn by acquisition channel
* Churn drivers

---

## Customer Risk

Displays:

* High-risk customers
* Churn probability
* MRR at risk
* Risk level
* Key risk factors

---

# 19. Technology Stack

## Programming

* Python 3.14.6

## Data Analysis

* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn
* Plotly

## Machine Learning

* Scikit-learn
* XGBoost
* SHAP

## Application

* Streamlit

## Development

* VS Code
* Jupyter
* Git
* GitHub

## Testing

* Pytest

---

# 20. Installation

## Clone the Repository

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd saas-product-analytics-churn-prediction
```

---

## Create Virtual Environment

The project uses a Python virtual environment.

```bash
python -m venv .venv
```

---

## Activate Environment

Because this project is being developed using **Windows Command Prompt**, activate the environment using:

```cmd
.venv\Scripts\activate
```

You should see:

```text
(.venv)
```

in the terminal.

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 21. Running Jupyter

Start Jupyter Notebook with:

```bash
jupyter notebook
```

Or use VS Code's built-in notebook support.

Make sure the selected Python interpreter is:

```text
.venv\Scripts\python.exe
```

---

# 22. Running the Streamlit Application

Once the application is completed:

```cmd
streamlit run app\app.py
```

The Streamlit dashboard will then open in the browser.

---

# 23. Testing

Run all tests with:

```bash
pytest
```

Run a specific test file:

```cmd
pytest tests\test_data_loader.py
```

---

# 24. Reproducibility

The project will maintain:

* A fixed project structure
* A `requirements.txt` file
* Consistent random seeds
* Reusable preprocessing functions
* Modular feature engineering
* Saved machine-learning models
* Documented analytical methodology

This allows the project to be reproduced on another machine.

---

# 25. Data Quality

Before modeling, the project will validate the following areas.

## Uniqueness

* Primary keys
* Duplicate records

## Missing Values

* Null counts
* Missing critical identifiers
* Missing timestamps

## Data Types

* Dates
* Numeric fields
* Boolean fields
* Categorical fields

## Referential Integrity

```text
events.user_id
        ↓
users.user_id

subscriptions.user_id
        ↓
users.user_id

support_tickets.user_id
        ↓
users.user_id
```

## Business Rules

Examples:

```text
resolution_time_hours >= 0

monthly_recurring_revenue >= 0

satisfaction_score ∈ [1, 5]

engagement_propensity ∈ [0, 1]
```

---

# 26. Expected Business Outcomes

The completed project should provide answers to questions such as:

* Which customers are most likely to churn?
* Why are they likely to churn?
* How does product engagement affect retention?
* Which features are associated with customer retention?
* Does poor support experience increase churn?
* Which customers generate the most revenue?
* How much revenue is currently at risk?
* Which customers should the retention team contact first?

---

# 27. Example Business Output

A final customer-risk table may look like:

| User      | Plan         |  MRR | Churn Probability | Risk     | Revenue at Risk |
| --------- | ------------ | ---: | ----------------: | -------- | --------------: |
| `U000123` | Enterprise   | $499 |              0.87 | Critical |         $434.13 |
| `U000451` | Professional | $199 |              0.74 | High     |         $147.26 |
| `U001208` | Starter      |  $49 |              0.63 | High     |          $30.87 |
| `U003421` | Professional | $199 |              0.28 | Low      |          $55.72 |

This allows the business to prioritize customers using both:

```text
Churn Risk
      +
Revenue Impact
```

rather than simply contacting every customer with the same retention strategy.

---

# 28. Project Development Roadmap

The project will be developed systematically.

```text
Phase 1
Environment Setup
        ↓
Phase 2
Data Validation
        ↓
Phase 3
Exploratory Data Analysis
        ↓
Phase 4
Product Analytics
        ↓
Phase 5
Funnel Analysis
        ↓
Phase 6
Retention & Cohort Analysis
        ↓
Phase 7
Revenue Analytics
        ↓
Phase 8
Support Analytics
        ↓
Phase 9
Churn Analysis
        ↓
Phase 10
Feature Engineering
        ↓
Phase 11
Machine Learning
        ↓
Phase 12
Model Evaluation
        ↓
Phase 13
Explainability
        ↓
Phase 14
Customer Risk Scoring
        ↓
Phase 15
Revenue at Risk
        ↓
Phase 16
Streamlit Dashboard
        ↓
Phase 17
Testing
        ↓
Phase 18
Documentation
```

---

# 29. Portfolio Value

This project demonstrates practical skills in:

* Python
* Pandas
* NumPy
* Data Cleaning
* Exploratory Data Analysis
* Product Analytics
* Customer Analytics
* SaaS Metrics
* Cohort Analysis
* Retention Analysis
* Revenue Analytics
* Feature Engineering
* Classification
* XGBoost
* Model Evaluation
* SHAP
* Customer Risk Scoring
* Streamlit
* Data Visualization
* Business Intelligence
* Git/GitHub
* Software Project Structure
* Testing

The project is designed to demonstrate an **end-to-end analytics and machine-learning workflow**, rather than only training a model.

---

# 30. Important Disclaimer

All datasets used in this project are **synthetically generated**.

They do not contain:

* Real customer information
* Real company information
* Confidential business data

The purpose of the datasets is to simulate a realistic SaaS product analytics environment for **learning and portfolio development**.

---

# 31. Documentation

| Document                | Description                               |
| ----------------------- | ----------------------------------------- |
| `README.md`             | Project overview and setup                |
| `data_dictionary.md`    | Dataset and column definitions            |
| `data_model.md`         | Data relationships and analytical model   |
| `business_questions.md` | Business questions and analytical roadmap |
| `requirements.txt`      | Python dependencies                       |

Additional documentation will be added as the project develops.

---

# 32. Final Objective

The ultimate goal of this project is to answer:

> **Who are our customers, how are they using our product, what drives engagement and retention, why do customers churn, which customers are most likely to leave, and how much revenue is at risk?**

The final solution will combine:

```text
Data Analytics
      +
Product Analytics
      +
Customer Analytics
      +
Machine Learning
      +
Explainable AI
      +
Business Intelligence
      +
Interactive Dashboard
```

to create a practical **SaaS Customer Intelligence and Churn Prediction Platform**.
