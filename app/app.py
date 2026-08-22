import streamlit as st
import pandas as pd

from data_loader import load_all_data

from utils import (
    format_currency,
    format_number,
    format_percentage,
)

from charts import (
    revenue_trend,
    revenue_by_plan,
    active_users_trend,
    churn_risk_distribution,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SaaS Product Analytics",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "📊 SaaS Product Analytics & Churn Prediction"
)

st.caption(
    "Product usage • Revenue • Retention • Churn • Customer Risk"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_all_data()

monthly_revenue = data["monthly_revenue"]
revenue_plan = data["revenue_by_plan"]
daily_product = data["daily_product_metrics"]
churn_risk = data["churn_risk"]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Dashboard")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Executive Overview",
        "Product Analytics",
        "Revenue Analytics",
        "Retention",
        "Churn & Risk",
        "Model Explainability",
    ],
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.header("Executive Overview")

    # --------------------------------------------------------
    # Revenue KPI
    # --------------------------------------------------------

    latest_mrr = 0

    if not monthly_revenue.empty:

        mrr_column = (
            "mrr"
            if "mrr" in monthly_revenue.columns
            else "monthly_recurring_revenue"
        )

        if mrr_column in monthly_revenue.columns:

            latest_mrr = monthly_revenue[
                mrr_column
            ].iloc[-1]

    # --------------------------------------------------------
    # Customer KPI
    # --------------------------------------------------------

    customers = 0

    if not churn_risk.empty:

        if "user_id" in churn_risk.columns:

            customers = churn_risk[
                "user_id"
            ].nunique()

    # --------------------------------------------------------
    # Churn KPI
    # --------------------------------------------------------

    average_risk = 0

    if not churn_risk.empty:

        if "churn_probability" in churn_risk.columns:

            average_risk = churn_risk[
                "churn_probability"
            ].mean()

    # --------------------------------------------------------
    # Active users
    # --------------------------------------------------------

    active_users = 0

    if not daily_product.empty:

        if "dau" in daily_product.columns:

            active_users = daily_product[
                "dau"
            ].iloc[-1]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Latest MRR",
        format_currency(latest_mrr),
    )

    col2.metric(
        "Customers",
        format_number(customers),
    )

    col3.metric(
        "Latest DAU",
        format_number(active_users),
    )

    col4.metric(
        "Average Churn Risk",
        format_percentage(average_risk),
    )

    st.divider()

    # --------------------------------------------------------
    # Revenue Trend
    # --------------------------------------------------------

    if not monthly_revenue.empty:

        st.subheader(
            "Revenue Trend"
        )

        try:

            st.plotly_chart(
                revenue_trend(
                    monthly_revenue
                ),
                use_container_width=True,
            )

        except Exception as exc:

            st.warning(
                f"Revenue chart unavailable: {exc}"
            )


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

elif page == "Product Analytics":

    st.header(
        "📈 Product Analytics"
    )

    if daily_product.empty:

        st.warning(
            "Product analytics data is not available."
        )

    else:

        if "dau" in daily_product.columns:

            st.plotly_chart(
                active_users_trend(
                    daily_product
                ),
                use_container_width=True,
            )

        st.subheader(
            "Product Metrics"
        )

        st.dataframe(
            daily_product.tail(30),
            use_container_width=True,
        )


# ============================================================
# REVENUE ANALYTICS
# ============================================================

elif page == "Revenue Analytics":

    st.header(
        "💰 Revenue Analytics"
    )

    if not monthly_revenue.empty:

        mrr_column = (
            "mrr"
            if "mrr" in monthly_revenue.columns
            else "monthly_recurring_revenue"
        )

        latest_mrr = monthly_revenue[
            mrr_column
        ].iloc[-1]

        arr = latest_mrr * 12

        col1, col2 = st.columns(2)

        col1.metric(
            "Latest MRR",
            format_currency(
                latest_mrr
            ),
        )

        col2.metric(
            "Estimated ARR",
            format_currency(
                arr
            ),
        )

        st.plotly_chart(
            revenue_trend(
                monthly_revenue
            ),
            use_container_width=True,
        )

    st.subheader(
        "Revenue by Plan"
    )

    if not revenue_plan.empty:

        try:

            st.plotly_chart(
                revenue_by_plan(
                    revenue_plan
                ),
                use_container_width=True,
            )

        except Exception as exc:

            st.warning(
                f"Plan chart unavailable: {exc}"
            )

        st.dataframe(
            revenue_plan,
            use_container_width=True,
        )


# ============================================================
# RETENTION
# ============================================================

elif page == "Retention":

    st.header(
        "🔄 Retention & Cohort Analysis"
    )

    retention = data["retention"]
    cohort = data["cohort_retention"]

    if retention.empty and cohort.empty:

        st.warning(
            "Retention data is not available."
        )

    else:

        if not retention.empty:

            st.subheader(
                "Retention Metrics"
            )

            st.dataframe(
                retention,
                use_container_width=True,
            )

        if not cohort.empty:

            st.subheader(
                "Cohort Retention"
            )

            st.dataframe(
                cohort,
                use_container_width=True,
            )


# ============================================================
# CHURN & RISK
# ============================================================

elif page == "Churn & Risk":

    st.header(
        "⚠️ Churn Risk Analysis"
    )

    if churn_risk.empty:

        st.warning(
            "Churn prediction data is not available."
        )

    else:

        # ----------------------------------------------------
        # Average Risk
        # ----------------------------------------------------

        if (
            "churn_probability"
            in churn_risk.columns
        ):

            average_risk = churn_risk[
                "churn_probability"
            ].mean()

            high_risk = (
                churn_risk[
                    "churn_probability"
                ] >= 0.70
            ).sum()

            col1, col2 = st.columns(2)

            col1.metric(
                "Average Churn Risk",
                format_percentage(
                    average_risk
                ),
            )

            col2.metric(
                "High-Risk Customers",
                format_number(
                    high_risk
                ),
            )

            st.plotly_chart(
                churn_risk_distribution(
                    churn_risk
                ),
                use_container_width=True,
            )

        # ----------------------------------------------------
        # Customer Risk Table
        # ----------------------------------------------------

        st.subheader(
            "Customer Risk"
        )

        display_columns = [
            column
            for column in [
                "user_id",
                "churn_probability",
                "risk_segment",
                "monthly_recurring_revenue",
            ]
            if column in churn_risk.columns
        ]

        if display_columns:

            risk_table = (
                churn_risk[
                    display_columns
                ]
                .sort_values(
                    "churn_probability",
                    ascending=False,
                )
                .head(50)
            )

            st.dataframe(
                risk_table,
                use_container_width=True,
            )


# ============================================================
# MODEL EXPLAINABILITY
# ============================================================

elif page == "Model Explainability":

    st.header(
        "🧠 Model Explainability"
    )

    shap_data = data[
        "shap_importance"
    ]

    global_data = data[
        "global_importance"
    ]

    if (
        shap_data.empty
        and global_data.empty
    ):

        st.warning(
            "Model explainability data is not available."
        )

    else:

        if not shap_data.empty:

            st.subheader(
                "Top Churn Drivers"
            )

            st.dataframe(
                shap_data.head(20),
                use_container_width=True,
            )

        if not global_data.empty:

            st.subheader(
                "Global Feature Importance"
            )

            st.dataframe(
                global_data.head(20),
                use_container_width=True,
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SaaS Product Analytics & Churn Prediction | "
    "Python • Pandas • Machine Learning • Streamlit"
)