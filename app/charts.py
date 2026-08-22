import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# REVENUE TREND
# ============================================================

def revenue_trend(df):

    fig = px.line(
        df,
        x="month",
        y="mrr",
        title="Monthly Recurring Revenue",
        markers=True,
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="MRR",
    )

    return fig


# ============================================================
# REVENUE BY PLAN
# ============================================================

def revenue_by_plan(df):

    fig = px.bar(
        df,
        x="plan",
        y="total_mrr",
        title="Revenue by Plan",
    )

    fig.update_layout(
        xaxis_title="Plan",
        yaxis_title="MRR",
    )

    return fig


# ============================================================
# PRODUCT USERS
# ============================================================

def active_users_trend(df):

    fig = px.line(
        df,
        x="date",
        y="dau",
        title="Daily Active Users",
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Active Users",
    )

    return fig


# ============================================================
# FEATURE ADOPTION
# ============================================================

def feature_adoption_chart(df):

    fig = px.bar(
        df,
        x="feature",
        y="adoption_rate",
        title="Feature Adoption",
    )

    fig.update_layout(
        xaxis_title="Feature",
        yaxis_title="Adoption Rate",
    )

    return fig


# ============================================================
# RETENTION
# ============================================================

def retention_chart(df):

    fig = px.line(
        df,
        x="period",
        y="retention_rate",
        color="cohort",
        title="Retention by Cohort",
    )

    fig.update_layout(
        xaxis_title="Period",
        yaxis_title="Retention Rate",
    )

    return fig


# ============================================================
# CHURN RISK
# ============================================================

def churn_risk_distribution(df):

    fig = px.histogram(
        df,
        x="churn_probability",
        nbins=20,
        title="Churn Risk Distribution",
    )

    fig.update_layout(
        xaxis_title="Churn Probability",
        yaxis_title="Customers",
    )

    return fig


# ============================================================
# CHURN RISK SEGMENTS
# ============================================================

def risk_segment_chart(df):

    fig = px.bar(
        df,
        x="risk_segment",
        y="customers",
        title="Customers by Risk Segment",
    )

    fig.update_layout(
        xaxis_title="Risk Segment",
        yaxis_title="Customers",
    )

    return fig


# ============================================================
# TOP RISK CUSTOMERS
# ============================================================

def top_risk_customers_chart(
    df,
    n=10,
):

    data = (
        df
        .sort_values(
            "churn_probability",
            ascending=False,
        )
        .head(n)
    )

    fig = px.bar(
        data,
        x="churn_probability",
        y="user_id",
        orientation="h",
        title="Highest-Risk Customers",
    )

    fig.update_layout(
        xaxis_title="Churn Probability",
        yaxis_title="Customer",
    )

    return fig


# ============================================================
# SHAP FEATURE IMPORTANCE
# ============================================================

def shap_importance_chart(
    df,
    n=15,
):

    data = (
        df
        .sort_values(
            "shap_value",
            key=abs,
            ascending=False,
        )
        .head(n)
    )

    fig = px.bar(
        data,
        x="shap_value",
        y="feature",
        orientation="h",
        title="Top Churn Drivers",
    )

    fig.update_layout(
        xaxis_title="SHAP Value",
        yaxis_title="Feature",
    )

    return fig