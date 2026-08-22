# Streamlit Application Documentation

## 1. Overview

This project includes an interactive **Streamlit dashboard** for exploring SaaS product analytics and customer behavior.

The Streamlit application provides a user-friendly interface for viewing the analytics generated from the project's processed CSV files.

The dashboard is designed to help answer key business questions related to:

* User activity
* Customer behavior
* Subscription performance
* Revenue
* Churn
* Product usage
* Support activity
* Customer segments
* Business KPIs

The application uses the project's generated analytics CSV files rather than performing complex analysis directly inside the dashboard.

---

## 2. Application Technology

The dashboard is built using:

* Python
* Streamlit
* Pandas
* Plotly
* CSV-based analytics outputs

### Main Application

```text
app/app.py
```

The Streamlit application is launched from this file.

---

## 3. Project Structure

The relevant application structure is:

```text
SaaS Product Analytics & Churn Prediction/
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── data_loader.py
│   ├── data_validation.py
│   └── preprocessing.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
├── notebooks/
│
├── src/
│
├── documentation/
│
├── requirements.txt
├── README.md
├── data_dictionary.md
├── data_model.md
├── business_questions.md
├── insights.md
└── streamlit_app.md
```

> The exact folder structure may vary depending on the final repository organization.

---

## 4. Requirements

Make sure Python is installed before running the application.

The main Python packages required by the dashboard are:

```text
streamlit
pandas
plotly
```

Additional project dependencies should be installed from:

```text
requirements.txt
```

---

## 5. Installation

Open **Command Prompt** and navigate to the project root directory.

Example:

```cmd
cd "C:\Users\user\Desktop\Data Analysis Projects\SaaS Product Analytics & Churn Prediction"
```

Install the project dependencies:

```cmd
pip install -r requirements.txt
```

If Streamlit is not installed, it can be installed with:

```cmd
pip install streamlit
```

---

## 6. Running the Application

From the project root directory, run:

```cmd
streamlit run app\app.py
```

Streamlit will start a local web server.

The application can then be opened in a web browser using the local URL displayed in the terminal.

Typically, Streamlit uses:

```text
http://localhost:8501
```

---

## 7. Dashboard Workflow

The application follows this general workflow:

```text
Analytics CSV Files
        ↓
Data Loading
        ↓
Data Validation
        ↓
Dashboard
        ↓
Filters / KPIs / Charts
        ↓
Business Insights
```

The dashboard does not require the user to manually manipulate the underlying CSV files.

---

## 8. Data Loading

The application uses the project's data-loading functionality to read the required analytics files.

The primary data-loading module is:

```text
app/data_loader.py
```

This keeps data-loading logic separate from the Streamlit interface.

The application can therefore load the generated analytics datasets and make them available to the dashboard.

---

## 9. Data Validation

Data validation is handled separately from the dashboard presentation layer.

The relevant module is:

```text
app/data_validation.py
```

Validation helps identify potential issues such as:

* Missing columns
* Missing values
* Unexpected data types
* Empty datasets
* Invalid data structures

This separation makes the application easier to maintain.

---

## 10. Preprocessing

Additional data preparation logic is maintained in:

```text
app/preprocessing.py
```

Preprocessing may include operations required before displaying the analytics in the dashboard.

Examples include:

* Date conversion
* Column preparation
* Data filtering
* Aggregation
* Formatting

---

# 11. Dashboard Components

The Streamlit application presents the project's main analytical results through interactive dashboard components.

## 11.1 KPI Summary

The KPI section provides a high-level overview of the SaaS business.

Typical KPIs include:

* Total Users
* Active Users
* Paying Customers
* Monthly Recurring Revenue
* Annual Recurring Revenue
* Customer Churn Rate
* Average Revenue
* Total Subscriptions

These KPIs provide an executive-level overview before users explore detailed charts.

---

## 11.2 User Analysis

The user analysis section helps understand the overall user base.

Possible analysis areas include:

* Total users
* Active vs inactive users
* User distribution
* User activity
* User growth
* Customer segments

The purpose is to identify changes in the customer base and overall product engagement.

---

## 11.3 Subscription Analysis

Subscription analysis focuses on customer subscription behavior.

Possible metrics include:

* Subscription counts
* Subscription plans
* Active subscriptions
* Cancelled subscriptions
* Subscription revenue
* Subscription trends

This section helps evaluate the performance of different subscription plans.

---

## 11.4 Revenue Analysis

Revenue analysis focuses on the financial performance of the SaaS product.

The dashboard can present:

* Monthly revenue
* MRR
* ARR
* Revenue by plan
* Revenue trends
* Customer revenue
* Revenue contribution

Revenue trends can help identify periods of growth or decline.

---

## 11.5 Churn Analysis

Churn analysis is one of the key components of the project.

The dashboard can be used to examine:

* Overall churn rate
* Churned customers
* Churn over time
* Churn by subscription plan
* Churn by customer segment
* Churn-related behavior

The objective is to identify customer groups that may have a higher risk of leaving the platform.

---

## 11.6 Product Usage Analysis

Product usage analysis examines how customers interact with the SaaS platform.

Possible metrics include:

* Total events
* Events per user
* Active users
* Feature usage
* Usage frequency
* Usage by customer segment

This analysis helps connect product engagement with customer behavior.

---

## 11.7 Support Analysis

Support-ticket information can be used to understand customer service activity.

Possible analysis includes:

* Total support tickets
* Tickets by category
* Tickets by priority
* Ticket resolution
* Average resolution time
* Support activity by customer segment

This can help identify whether support activity is associated with customer retention or churn.

---

# 12. Dashboard Filters

Where available, dashboard filters allow users to interactively explore the data.

Typical filters may include:

* Date
* Subscription plan
* Customer segment
* User status
* Churn status
* Event type
* Support category

Changing a filter updates the relevant dashboard metrics and visualizations.

---

# 13. Charts and Visualizations

The application uses charts to make analytical results easier to understand.

Common visualization types include:

### Line Charts

Used for:

* Revenue trends
* User growth
* Churn trends
* Monthly activity

### Bar Charts

Used for:

* Revenue by plan
* Customers by segment
* Usage by feature
* Tickets by category

### Pie / Donut Charts

Used for:

* Customer distribution
* Subscription distribution
* Active vs inactive users

### KPI Cards

Used for:

* Revenue
* Users
* Customers
* Churn
* Subscriptions

The goal is to keep the dashboard focused on business interpretation rather than unnecessary visual complexity.

---

# 14. Analytics CSV Architecture

The Streamlit dashboard uses generated analytics CSV files as its analytical input.

The general architecture is:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Data Processing
   ↓
Analytics Generation
   ↓
Analytics CSV Files
   ↓
Streamlit Dashboard
```

This approach separates:

**Data processing**

from

**Dashboard presentation**

which makes the project easier to maintain and debug.

---

# 15. Column-Name Errors

The dashboard charts depend on the actual columns available in the generated analytics CSV files.

If a chart produces an error such as:

```text
KeyError: 'column_name'
```

or:

```text
ColumnNotFoundError
```

do not guess or manually rename columns immediately.

Instead:

1. Copy the complete error message.
2. Identify which chart caused the error.
3. Check the corresponding analytics CSV.
4. Compare the chart code with the actual CSV column names.
5. Update the chart using the real schema.

For example:

```text
Expected:

monthly_revenue

Actual:

total_revenue
```

The dashboard code should be updated to use:

```python
df["total_revenue"]
```

rather than changing the analytics dataset unnecessarily.

This keeps the analytics pipeline consistent.

---

# 16. Troubleshooting

## Streamlit Command Not Found

If Command Prompt shows:

```text
'streamlit' is not recognized as an internal or external command
```

install Streamlit:

```cmd
pip install streamlit
```

Then run:

```cmd
streamlit run app\app.py
```

---

## ModuleNotFoundError

If the application reports an import error, verify that the command is being executed from the project root.

Example:

```cmd
cd "C:\Users\user\Desktop\Data Analysis Projects\SaaS Product Analytics & Churn Prediction"
```

Then:

```cmd
streamlit run app\app.py
```

Also verify that the referenced Python modules exist inside the expected directories.

---

## FileNotFoundError

A missing CSV error usually means that the application cannot locate one of the expected analytics files.

Check:

* The analytics CSV exists.
* The filename is correct.
* The folder path is correct.
* The application is being launched from the project root.
* The path used by the application matches the actual project structure.

---

## Column-Name Error

If a chart fails because a column does not exist:

```text
KeyError: 'column_name'
```

use the actual generated analytics CSV schema.

Do not create assumed columns simply to make the chart run.

---

## Empty Chart

If a chart loads but contains no data, check:

* Whether the CSV contains rows.
* Whether filters are excluding all records.
* Whether date columns were parsed correctly.
* Whether the selected category exists in the dataset.
* Whether the aggregation produces valid values.

---

# 17. Application Design Principles

The dashboard follows several simple principles:

### Separation of Responsibilities

```text
Data Loading
     ↓
Validation
     ↓
Processing
     ↓
Dashboard
```

Each component has a specific responsibility.

### Reusable Data Logic

Data-loading and processing functions are kept outside the main Streamlit interface where possible.

### Business-Focused Visuals

Charts should answer business questions rather than simply display available columns.

### Minimal Complexity

The dashboard should remain easy to understand, maintain, and extend.

New functionality should only be added when it provides meaningful analytical value.

---

# 18. Running the Project Locally

The complete local workflow is:

```cmd
cd "C:\Users\user\Desktop\Data Analysis Projects\SaaS Product Analytics & Churn Prediction"
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

Run the dashboard:

```cmd
streamlit run app\app.py
```

Then open the local Streamlit URL shown in Command Prompt.

---

# 19. Recommended Usage

For the best workflow:

1. Run the analytics/data-generation pipeline first.
2. Confirm the analytics CSV files have been generated.
3. Run the Streamlit application.
4. Review the KPI summary.
5. Explore the dashboard sections.
6. Apply available filters.
7. Compare trends and segments.
8. Investigate unusual results.
9. Use the dashboard findings together with `insights.md` for the final business interpretation.

---

# 20. Final Application Status

The Streamlit dashboard has been successfully tested and is currently running.

The application provides an interactive interface for the project's generated SaaS analytics and allows the analytical results to be explored without directly working with the underlying CSV files.

The dashboard is intentionally kept focused on the project's existing analytics pipeline rather than introducing additional unnecessary complexity.

---

## 21. Quick Reference

| Task                 | Command                           |
| -------------------- | --------------------------------- |
| Navigate to project  | `cd "PROJECT_ROOT"`               |
| Install dependencies | `pip install -r requirements.txt` |
| Run dashboard        | `streamlit run app\app.py`        |
| Local Streamlit URL  | `http://localhost:8501`           |

---

## 22. Documentation Summary

This file documents the Streamlit layer of the SaaS Product Analytics project.

The complete project workflow is:

```text
Raw SaaS Data
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
Feature / Metric Preparation
      ↓
Analytics CSV Generation
      ↓
Streamlit Dashboard
      ↓
Business Insights
```

The dashboard serves as the final interactive presentation layer of the project.
