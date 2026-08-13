# Data Model

## SaaS Product Analytics & Churn Prediction

This document describes the analytical data model used in the SaaS Product Analytics & Churn Prediction project.

The model integrates user profiles, product usage events, subscription information, and customer support interactions to support:

- Product analytics
- User engagement analysis
- Funnel analysis
- Retention and cohort analysis
- Revenue analytics
- Customer churn analysis
- Churn prediction
- Customer risk scoring

---

# 1. Data Model Overview

The project uses four primary datasets:

| Dataset | Role | Grain | Primary Key |
|---|---|---|---|
| `users.csv` | User Dimension | One row per user | `user_id` |
| `events.csv` | Product Usage Fact | One row per event | `event_id` |
| `subscriptions.csv` | Subscription Fact | One row per subscription | `subscription_id` |
| `support_tickets.csv` | Support Fact | One row per ticket | `ticket_id` |

The central entity is the **user**.

```text
                         ┌─────────────────┐
                         │      USERS      │
                         │   30,000 rows   │
                         │                 │
                         │ PK: user_id     │
                         │ FK: company_id  │
                         └────────┬────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             │                    │                    │
             ▼                    ▼                    ▼
   ┌─────────────────┐  ┌─────────────────┐  ┌────────────────────┐
   │     EVENTS      │  │  SUBSCRIPTIONS  │  │  SUPPORT TICKETS   │
   │   1.55M+ rows   │  │   30,000 rows   │  │    9,976 rows      │
   │                 │  │                 │  │                    │
   │ PK: event_id    │  │ PK: sub_id      │  │ PK: ticket_id      │
   │ FK: user_id     │  │ FK: user_id     │  │ FK: user_id        │
   │ FK: company_id  │  │ FK: company_id  │  │ FK: company_id     │
   └─────────────────┘  └─────────────────┘  |
   
```


## 2. Entity Relationships

### 2.1 User → Events

**Relationship:**

```text
users.user_id
      │
      │ 1
      │
      │ N
      ▼
events.user_id
```

**Cardinality:** One-to-Many (1:N)

One user can generate many product events.

**Example:**

```text
User U000001
    │
    ├── Login
    ├── Project Created
    ├── Task Created
    ├── Task Completed
    ├── File Uploaded
    └── Report Generated
```

This relationship is the foundation for **product engagement analysis**.

---

## 3. User → Subscriptions

**Relationship:**

```text
users.user_id
      │
      │ 1
      │
      │ 1
      ▼
subscriptions.user_id
```

**Cardinality:** One-to-One (1:1)

In the current synthetic dataset design, each user has one subscription record representing their current subscription state and lifecycle.

> **Future extension:** The model can be extended to One-to-Many (1:N) if historical subscription versions are introduced.

**Example:**

```text
User U000001
      │
      └── Subscription
           ├── Plan: Professional
           ├── MRR: $79
           └── Status: Active
```

---

## 4. User → Support Tickets

**Relationship:**

```text
users.user_id
      │
      │ 1
      │
      │ N
      ▼
support_tickets.user_id
```

**Cardinality:** One-to-Many (1:N)

A user can create multiple support tickets.

**Example:**

```text
User U000001
      │
      ├── Ticket T000001
      ├── Ticket T000021
      ├── Ticket T000104
      └── Ticket T000501
```

This relationship allows us to investigate whether **support experience is associated with churn**.

---

# 5. Company Relationships

The datasets also contain `company_id`.

```text
users.company_id
        │
        ├──────── events.company_id
        │
        ├──────── subscriptions.company_id
        │
        └──────── support_tickets.company_id
```

A company can contain multiple users.

Therefore:

```text
Company
   │
   ├── User
   ├── User
   ├── User
   └── User
```

This allows both **user-level** and **company-level** analysis.

---

# 6. Company → Users

**Logical relationship:**

```text
company_id
     │
     │ 1
     │
     │ N
     ▼
users
```

**Cardinality:** One-to-Many (1:N)

One company can have multiple users.

This enables analysis such as:

* Users per company
* Company engagement
* Company-level churn
* Revenue by company
* Product adoption by company
* Enterprise account behavior

---

# 7. Company → Events

```text
company_id
     │
     │ 1
     │
     │ N
     ▼
events
```

One company can generate many product events through its users.

This allows us to calculate:

* Company activity
* Company engagement
* Active companies
* Events per company
* Feature adoption by company

---

# 8. Company → Subscriptions

```text
company_id
     │
     │ 1
     │
     │ N
     ▼
subscriptions
```

A company can be associated with subscription records through its users.

This allows analysis of:

* Revenue by company
* Company subscription plans
* Enterprise revenue
* Customer lifetime value
* Company churn

---

# 9. Company → Support Tickets

```text
company_id
     │
     │ 1
     │
     │ N
     ▼
support_tickets
```

One company can generate multiple support tickets.

This allows us to analyze:

* Support volume by company
* Support burden
* Average resolution time
* Satisfaction by company
* Support activity versus churn

---

# 10. Analytical Model

The project follows a simplified **fact-and-dimension analytical architecture**.

## Dimension

### `dim_user`

Based primarily on:

```text
users.csv
```

## Fact Tables

* `fact_events`
* `fact_subscriptions`
* `fact_support_tickets`

### Conceptual Model

```text
                       DIM_USER
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
     FACT_EVENTS    FACT_SUBSCRIPTIONS   FACT_SUPPORT
```

This structure makes it easier to aggregate behavioral and business metrics by user attributes.

---

# 11. Fact Table: Product Events

### Logical Table

`fact_events`

### Grain

> One row = one product event

### Primary Key

`event_id`

### Foreign Keys

* `user_id`
* `company_id`

### Important Measures

Examples:

* `event_count`
* `active_users`
* `active_days`
* `sessions`
* `session_duration`
* `feature_usage`

---

# 12. Fact Table: Subscriptions

### Logical Table

`fact_subscriptions`

### Grain

> One row = one subscription record

### Primary Key

`subscription_id`

### Foreign Keys

* `user_id`
* `company_id`

### Important Measures

* `monthly_recurring_revenue`
* `annual_contract_value`
* `upgrade_count`
* `downgrade_count`
* `tenure_days`

---

# 13. Fact Table: Support Tickets

### Logical Table

`fact_support_tickets`

### Grain

> One row = one support ticket

### Primary Key

`ticket_id`

### Foreign Keys

* `user_id`
* `company_id`

### Important Measures

* `resolution_time_hours`
* `satisfaction_score`
* `ticket_count`
* `reopened_ticket_count`

---

# 14. User-Level Analytical Dataset

For machine learning, the three fact tables will eventually be aggregated to the **user level**.

### Conceptual Flow

```text
                         USERS
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          EVENTS      SUBSCRIPTIONS   SUPPORT
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                    USER FEATURES
```

The resulting analytical dataset may contain features such as:

### User Attributes

* `user_id`
* `plan`
* `country`
* `industry`
* `company_size`
* `acquisition_channel`

### Engagement Features

* `total_events`
* `active_days`
* `session_count`
* `avg_session_duration`
* `feature_count`
* `feature_adoption_rate`
* `last_active_date`
* `days_since_last_activity`

### Subscription Features

* `subscription_tenure`
* `monthly_recurring_revenue`
* `upgrade_count`
* `downgrade_count`

### Support Features

* `ticket_count`
* `avg_resolution_time`
* `avg_satisfaction`
* `reopened_ticket_count`

### Target

* `churn`

---

# 15. Churn Modeling Dataset

The final machine-learning dataset will be built at the **user level**.

### Grain

> One row = one user

### Example

| Feature                     | Example |
| --------------------------- | ------: |
| `total_events`              |     147 |
| `active_days`               |      42 |
| `session_count`             |      31 |
| `feature_adoption_rate`     |    0.68 |
| `days_since_last_activity`  |       7 |
| `monthly_recurring_revenue` |      79 |
| `ticket_count`              |       3 |
| `avg_satisfaction`          |     4.0 |
| `upgrade_count`             |       1 |
| `downgrade_count`           |       0 |
| `churn`                     |       0 |

### Target Variable

The target variable will be:

`churn`

Where:

```text
1 = Churned
0 = Active
```

The exact target definition will be documented in the churn-analysis methodology.

---

# 16. Important Modeling Principle

## Avoiding Data Leakage

We must avoid **data leakage** when building the churn prediction model.

Information that occurs **after the churn event** should not be used as a predictive feature.

Examples include:

* `subscription_end_date`
* Post-churn events
* Post-churn support tickets
* Future activity
* Future revenue

Instead, features should be calculated using information that was available **before the prediction point**.

### Conceptual Modeling Timeline

```text
Historical Behavior
        │
        ▼
Feature Engineering
        │
        ▼
Prediction Date
        │
        ▼
Future Churn
```

This makes the model more realistic for an actual SaaS customer-retention use case.

---

# 17. Analytical Time Structure

The project will use event and subscription dates to create time-based metrics.

### Important Dates

* `signup_date`
* `event_timestamp`
* `subscription_start_date`
* `subscription_end_date`
* `created_at`
* `resolved_at`

These dates will support:

* Daily activity
* Weekly activity
* Monthly activity
* Cohort analysis
* Retention analysis
* Subscription tenure
* Churn timing
* Revenue trends

---

# 18. Core Analytical Relationships

The project will investigate the following relationships.

## Product Usage → Engagement → Retention → Revenue

```text
Product Usage
      │
      ▼
Engagement
      │
      ▼
Retention
      │
      ▼
Subscription
      │
      ▼
Revenue
```

## Support Experience → Churn Risk

```text
Support Experience
      │
      ▼
Customer Satisfaction
      │
      ▼
Engagement
      │
      ▼
Churn Risk
```

## Feature Adoption → Churn

```text
Feature Adoption
      │
      ▼
Engagement
      │
      ▼
Retention
      │
      ▼
Churn
```

These relationships will be investigated through descriptive analysis, statistical analysis, feature engineering, and machine-learning models.

---

# 19. Business-Level Model

The final analytical model connects four major business domains:

```text
┌─────────────────────────────────────────────────────┐
│                  SAAS CUSTOMER                      │
└──────────────────────┬──────────────────────────────┘
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
   PRODUCT          REVENUE          SUPPORT
   USAGE            & PLAN           EXPERIENCE
       │               │                │
       └───────────────┼────────────────┘
                       ▼
                  ENGAGEMENT
                       │
                       ▼
                   RETENTION
                       │
                       ▼
                     CHURN
                       │
                       ▼
              CHURN PREDICTION
```

This represents the project's overall analytical logic:

> **Product usage, revenue, subscription behavior, and support experience influence engagement and retention, which can ultimately be associated with customer churn.**

---

# 20. Model Objectives

The data model is designed to answer five major analytical questions.

## Product

**How are customers using the SaaS product?**

Analyze:

* Product events
* Feature usage
* Sessions
* Feature adoption
* User activity

## Engagement

**Which behaviors indicate highly engaged users?**

Analyze:

* Event frequency
* Active days
* Session activity
* Feature adoption
* Recency of activity

## Retention

**What factors contribute to long-term customer retention?**

Analyze:

* Cohort retention
* Engagement patterns
* Subscription tenure
* Product adoption
* Support experience

## Revenue

**Which customers, plans, and segments generate the most recurring revenue?**

Analyze:

* MRR
* ARR
* ARPU
* Subscription plans
* Upgrades
* Downgrades
* Customer segments

## Churn

**Which behavioral, subscription, and support factors are associated with customer churn?**

Analyze:

* Engagement decline
* Feature adoption
* Subscription behavior
* Support interactions
* Satisfaction
* Customer tenure

---

# Related Documentation

| Document                | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| `data_dictionary.md`    | Defines datasets and columns                   |
| `data_model.md`         | Defines relationships and analytical structure |
| `business_questions.md` | Defines business questions                     |
| `methodology.md`        | Defines analytical and modeling methodology    |
| `insights.md`           | Contains final findings and recommendations    |

---

# Data Source

All datasets are **synthetically generated** for this portfolio project.

They do not represent actual customers, companies, or production SaaS data.
