from pathlib import Path

import pandas as pd
import streamlit as st

from config.config import (
    ANALYTICS_DATA_DIR,
    MONTHLY_REVENUE_FILE,
    REVENUE_BY_PLAN_FILE,
    REVENUE_BY_BILLING_FILE,
    NEW_SUBSCRIPTIONS_FILE,
    CANCELLATIONS_FILE,
    CUSTOMER_REVENUE_FILE,
    REVENUE_CONCENTRATION_FILE,
    PLAN_SUMMARY_FILE,
    DAILY_PRODUCT_METRICS_FILE,
    FEATURE_ADOPTION_FILE,
    PRODUCT_USAGE_FILE,
    RETENTION_FILE,
    COHORT_RETENTION_FILE,
    CHURN_RISK_FILE,
    CHURN_SUMMARY_FILE,
    CHURN_FEATURES_FILE,
    HIGH_RISK_EXPLANATIONS_FILE,
    CHURN_PRIORITY_FILE,
    MODEL_GLOBAL_IMPORTANCE_FILE,
    MODEL_SHAP_IMPORTANCE_FILE,
)


# ============================================================
# GENERAL CSV LOADER
# ============================================================

def load_csv(
    file_path: Path,
    parse_dates=None,
    required=False,
):
    """
    Load a CSV file safely.

    Parameters
    ----------
    file_path : Path
        Path to CSV file.

    parse_dates : list, optional
        Columns that should be parsed as dates.

    required : bool
        If True, raise an error when file is missing.
        If False, return an empty DataFrame.

    Returns
    -------
    pandas.DataFrame
    """

    if not file_path.exists():

        message = (
            f"File not found: {file_path}"
        )

        if required:
            raise FileNotFoundError(
                message
            )

        st.warning(
            message
        )

        return pd.DataFrame()

    try:

        df = pd.read_csv(
            file_path,
            parse_dates=parse_dates,
        )

        return df

    except Exception as exc:

        st.error(
            f"Error loading {file_path.name}: "
            f"{exc}"
        )

        if required:
            raise

        return pd.DataFrame()


# ============================================================
# REVENUE DATA
# ============================================================

@st.cache_data
def load_monthly_revenue():

    return load_csv(
        MONTHLY_REVENUE_FILE
    )


@st.cache_data
def load_revenue_by_plan():

    return load_csv(
        REVENUE_BY_PLAN_FILE
    )


@st.cache_data
def load_revenue_by_billing():

    return load_csv(
        REVENUE_BY_BILLING_FILE
    )


@st.cache_data
def load_new_subscriptions():

    return load_csv(
        NEW_SUBSCRIPTIONS_FILE
    )


@st.cache_data
def load_cancellations():

    return load_csv(
        CANCELLATIONS_FILE
    )


@st.cache_data
def load_customer_revenue():

    return load_csv(
        CUSTOMER_REVENUE_FILE
    )


@st.cache_data
def load_revenue_concentration():

    return load_csv(
        REVENUE_CONCENTRATION_FILE
    )


@st.cache_data
def load_plan_summary():

    return load_csv(
        PLAN_SUMMARY_FILE
    )


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

@st.cache_data
def load_daily_product_metrics():

    return load_csv(
        DAILY_PRODUCT_METRICS_FILE
    )


@st.cache_data
def load_feature_adoption():

    return load_csv(
        FEATURE_ADOPTION_FILE
    )


@st.cache_data
def load_product_usage():

    return load_csv(
        PRODUCT_USAGE_FILE
    )


# ============================================================
# RETENTION
# ============================================================

@st.cache_data
def load_retention():

    return load_csv(
        RETENTION_FILE
    )


@st.cache_data
def load_cohort_retention():

    return load_csv(
        COHORT_RETENTION_FILE
    )


# ============================================================
# CHURN
# ============================================================

@st.cache_data
def load_churn_risk():

    return load_csv(
        CHURN_RISK_FILE
    )


@st.cache_data
def load_churn_summary():

    return load_csv(
        CHURN_SUMMARY_FILE
    )


@st.cache_data
def load_churn_features():

    return load_csv(
        CHURN_FEATURES_FILE
    )


@st.cache_data
def load_high_risk_explanations():

    return load_csv(
        HIGH_RISK_EXPLANATIONS_FILE
    )


@st.cache_data
def load_churn_priority():

    return load_csv(
        CHURN_PRIORITY_FILE
    )


# ============================================================
# MODEL EXPLAINABILITY
# ============================================================

@st.cache_data
def load_global_importance():

    return load_csv(
        MODEL_GLOBAL_IMPORTANCE_FILE
    )


@st.cache_data
def load_shap_importance():

    return load_csv(
        MODEL_SHAP_IMPORTANCE_FILE
    )


# ============================================================
# LOAD ALL DASHBOARD DATA
# ============================================================

@st.cache_data
def load_all_data():
    """
    Load all analytics datasets used by the dashboard.

    Returns
    -------
    dict
        Dictionary containing all dashboard datasets.
    """

    data = {

        # Revenue
        "monthly_revenue":
            load_monthly_revenue(),

        "revenue_by_plan":
            load_revenue_by_plan(),

        "revenue_by_billing":
            load_revenue_by_billing(),

        "new_subscriptions":
            load_new_subscriptions(),

        "cancellations":
            load_cancellations(),

        "customer_revenue":
            load_customer_revenue(),

        "revenue_concentration":
            load_revenue_concentration(),

        "plan_summary":
            load_plan_summary(),

        # Product
        "daily_product_metrics":
            load_daily_product_metrics(),

        "feature_adoption":
            load_feature_adoption(),

        "product_usage":
            load_product_usage(),

        # Retention
        "retention":
            load_retention(),

        "cohort_retention":
            load_cohort_retention(),

        # Churn
        "churn_risk":
            load_churn_risk(),

        "churn_summary":
            load_churn_summary(),

        "churn_features":
            load_churn_features(),

        "high_risk_explanations":
            load_high_risk_explanations(),

        "churn_priority":
            load_churn_priority(),

        # Explainability
        "global_importance":
            load_global_importance(),

        "shap_importance":
            load_shap_importance(),
    }

    return data


# ============================================================
# DATASET STATUS
# ============================================================

def get_dataset_status(
    data: dict,
):
    """
    Return row counts for all loaded datasets.
    """

    status = []

    for name, df in data.items():

        status.append(
            {
                "dataset": name,
                "rows": len(df),
                "columns": len(df.columns),
                "loaded": not df.empty,
            }
        )

    return pd.DataFrame(
        status
    )


# ============================================================
# DATASET SUMMARY
# ============================================================

def get_data_summary(
    data: dict,
):
    """
    Create a compact summary of dashboard datasets.
    """

    summary = []

    for name, df in data.items():

        if df.empty:

            summary.append(
                {
                    "dataset": name,
                    "rows": 0,
                    "columns": 0,
                }
            )

            continue

        summary.append(
            {
                "dataset": name,
                "rows": len(df),
                "columns": len(
                    df.columns
                ),
            }
        )

    return pd.DataFrame(
        summary
    )


# ============================================================
# VALIDATE DASHBOARD DATA
# ============================================================

def validate_dashboard_data(
    data: dict,
):
    """
    Validate whether the major datasets
    required by the dashboard are available.
    """

    required_datasets = [
        "monthly_revenue",
        "daily_product_metrics",
        "churn_risk",
    ]

    missing = []

    for dataset in required_datasets:

        if (
            dataset not in data
            or data[dataset].empty
        ):

            missing.append(
                dataset
            )

    return missing


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print(
        "SAAS DASHBOARD DATA LOADER"
    )
    print("=" * 70)

    print(
        "\nAnalytics directory:"
    )

    print(
        ANALYTICS_DATA_DIR
    )

    print(
        "\nThis module is designed to be "
        "used by Streamlit."
    )

    print(
        "\nAvailable loader functions:"
    )

    print(
        "- load_monthly_revenue()"
    )

    print(
        "- load_revenue_by_plan()"
    )

    print(
        "- load_daily_product_metrics()"
    )

    print(
        "- load_retention()"
    )

    print(
        "- load_churn_risk()"
    )

    print(
        "- load_churn_summary()"
    )

    print(
        "- load_high_risk_explanations()"
    )

    print(
        "- load_global_importance()"
    )

    print(
        "- load_shap_importance()"
    )

    print(
        "- load_all_data()"
    )