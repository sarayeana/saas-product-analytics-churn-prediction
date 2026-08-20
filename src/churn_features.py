"""
SaaS Churn Feature Engineering
==============================

Purpose
-------
Create a customer-level machine-learning dataset for SaaS churn
prediction.

This module combines:

    1. Subscription information
    2. Revenue information
    3. Product usage information
    4. Customer engagement information

Output
------
data/analytics/churn_features.csv

Important
---------
The churn target is created from subscription status/end date.

Direct leakage fields such as subscription_end_date are NOT used
as model features.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# =====================================================================
# PROJECT PATHS
# =====================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


# =====================================================================
# LOAD SUBSCRIPTIONS
# =====================================================================

def load_subscriptions():
    """Load processed subscription data."""

    path = PROCESSED_DIR / "subscriptions.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Subscriptions file not found:\n{path}"
        )

    df = pd.read_csv(path)

    print(
        f"Subscriptions loaded: {len(df):,}"
    )

    return df


# =====================================================================
# PREPARE SUBSCRIPTIONS
# =====================================================================

def prepare_subscriptions(df):
    """Prepare subscription data."""

    df = df.copy()

    # ---------------------------------------------------------------
    # Dates
    # ---------------------------------------------------------------

    df["subscription_start_date"] = pd.to_datetime(
        df["subscription_start_date"],
        errors="coerce"
    )

    df["subscription_end_date"] = pd.to_datetime(
        df["subscription_end_date"],
        errors="coerce"
    )

    # ---------------------------------------------------------------
    # Numeric columns
    # ---------------------------------------------------------------

    numeric_columns = [
        "monthly_recurring_revenue",
        "annual_contract_value",
        "upgrade_count",
        "downgrade_count",
        "tenure_days",
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # ---------------------------------------------------------------
    # Text columns
    # ---------------------------------------------------------------

    text_columns = [
        "plan",
        "billing_frequency",
        "status",
        "acquisition_source",
        "trial",
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .str.lower()
            )

    return df


# =====================================================================
# CREATE CHURN TARGET
# =====================================================================

def create_churn_target(df):
    """
    Create the binary churn target.

    churn = 1 -> churned
    churn = 0 -> retained
    """

    df = df.copy()

    df["churn"] = (
        df["subscription_end_date"]
        .notna()
        .astype(int)
    )

    # Use subscription status as an additional signal.

    if "status" in df.columns:

        churn_statuses = {
            "churned",
            "cancelled",
            "canceled",
            "terminated",
            "expired",
            "inactive",
        }

        status_churn = (
            df["status"]
            .isin(churn_statuses)
        )

        df.loc[
            status_churn,
            "churn"
        ] = 1

    return df


# =====================================================================
# SUBSCRIPTION FEATURES
# =====================================================================

def create_subscription_features(df):
    """
    Create subscription-level predictive features.

    Leakage fields are deliberately excluded.
    """

    features = pd.DataFrame()

    features["user_id"] = df["user_id"]

    # ---------------------------------------------------------------
    # Categorical subscription features
    # ---------------------------------------------------------------

    features["plan"] = df["plan"]

    features["billing_frequency"] = (
        df["billing_frequency"]
    )

    features["trial"] = df["trial"]

    features["acquisition_source"] = (
        df["acquisition_source"]
    )

    # ---------------------------------------------------------------
    # Revenue
    # ---------------------------------------------------------------

    features["monthly_recurring_revenue"] = (
        df["monthly_recurring_revenue"]
    )

    features["annual_contract_value"] = (
        df["annual_contract_value"]
    )

    # ---------------------------------------------------------------
    # Subscription behavior
    # ---------------------------------------------------------------

    features["tenure_days"] = (
        df["tenure_days"]
    )

    features["upgrade_count"] = (
        df["upgrade_count"]
    )

    features["downgrade_count"] = (
        df["downgrade_count"]
    )

    # ---------------------------------------------------------------
    # Upgrade / downgrade ratio
    # ---------------------------------------------------------------

    features["upgrade_downgrade_ratio"] = np.where(
        df["downgrade_count"] > 0,
        df["upgrade_count"]
        / df["downgrade_count"],
        df["upgrade_count"],
    )

    return features


# =====================================================================
# REVENUE FEATURES
# =====================================================================

def load_revenue_features():
    """
    Load customer-level revenue analytics produced by
    revenue_metrics.py.
    """

    path = (
        ANALYTICS_DIR
        / "customer_revenue.csv"
    )

    if not path.exists():

        print(
            "\nWARNING:"
            "\ncustomer_revenue.csv was not found."
            "\nRevenue features will be skipped."
        )

        return None

    df = pd.read_csv(path)

    print(
        f"Customer revenue records: "
        f"{len(df):,}"
    )

    return df


def create_revenue_features(
    subscription_features,
    revenue_df
):
    """
    Merge customer-level revenue features.
    """

    if revenue_df is None:

        return subscription_features

    revenue_columns = [
        "user_id",
        "total_mrr",
        "average_monthly_revenue",
        "active_months",
        "plans_used",
        "estimated_annual_value",
    ]

    available_columns = [
        column
        for column in revenue_columns
        if column in revenue_df.columns
    ]

    revenue = revenue_df[
        available_columns
    ].copy()

    result = subscription_features.merge(
        revenue,
        on="user_id",
        how="left",
    )

    return result


# =====================================================================
# PRODUCT USAGE FEATURES
# =====================================================================

def find_product_feature_file():
    """
    Look for feature-engineering output files.

    The function checks several likely filenames because the
    feature_engineering module may produce different output names.
    """

    possible_files = [
        "user_features.csv",
        "user_level_features.csv",
        "customer_features.csv",
        "user_feature_engineered.csv",
        "user_features_engineered.csv",
    ]

    for filename in possible_files:

        path = (
            ANALYTICS_DIR
            / filename
        )

        if path.exists():

            return path

    return None


def load_product_features():
    """
    Load user-level product features if available.
    """

    path = find_product_feature_file()

    if path is None:

        print(
            "\nWARNING:"
            "\nNo product feature file was found."
            "\nSubscription and revenue features will be used."
        )

        return None

    print(
        f"\nProduct feature file found:"
        f"\n{path.name}"
    )

    df = pd.read_csv(path)

    print(
        f"Product feature records: "
        f"{len(df):,}"
    )

    return df


def create_product_features(
    customer_features,
    product_df
):
    """
    Merge product usage features.

    Only numerical user-level product metrics are added.
    """

    if product_df is None:

        return customer_features

    if "user_id" not in product_df.columns:

        print(
            "WARNING: Product feature file does not contain user_id."
        )

        return customer_features

    product = product_df.copy()

    # ---------------------------------------------------------------
    # Remove obvious target/leakage fields
    # ---------------------------------------------------------------

    leakage_columns = [
        "churn",
        "subscription_end_date",
        "end_date",
        "status",
    ]

    product = product.drop(
        columns=[
            column
            for column in leakage_columns
            if column in product.columns
        ],
        errors="ignore",
    )

    # ---------------------------------------------------------------
    # Keep user_id + numeric columns
    # ---------------------------------------------------------------

    numeric_columns = product.select_dtypes(
        include=np.number
    ).columns.tolist()

    numeric_columns = [
        column
        for column in numeric_columns
        if column != "user_id"
    ]

    if not numeric_columns:

        print(
            "WARNING: No numerical product features found."
        )

        return customer_features

    product = product[
        ["user_id"] + numeric_columns
    ]

    # ---------------------------------------------------------------
    # Avoid duplicate column names
    # ---------------------------------------------------------------

    existing_columns = set(
        customer_features.columns
    )

    columns_to_add = [
        column
        for column in product.columns
        if (
            column == "user_id"
            or column not in existing_columns
        )
    ]

    product = product[
        columns_to_add
    ]

    result = customer_features.merge(
        product,
        on="user_id",
        how="left",
    )

    return result


# =====================================================================
# CREATE DERIVED FEATURES
# =====================================================================

def create_derived_features(df):
    """
    Create additional ML-friendly features.
    """

    df = df.copy()

    # ---------------------------------------------------------------
    # Revenue per active month
    # ---------------------------------------------------------------

    if {
        "total_mrr",
        "active_months",
    }.issubset(df.columns):

        df["revenue_per_active_month"] = np.where(
            df["active_months"] > 0,
            df["total_mrr"]
            / df["active_months"],
            0,
        )

    # ---------------------------------------------------------------
    # Tenure in months
    # ---------------------------------------------------------------

    if "tenure_days" in df.columns:

        df["tenure_months"] = (
            df["tenure_days"]
            / 30.44
        )

    # ---------------------------------------------------------------
    # Upgrade activity
    # ---------------------------------------------------------------

    if "upgrade_count" in df.columns:

        df["has_upgrade"] = (
            df["upgrade_count"] > 0
        ).astype(int)

    # ---------------------------------------------------------------
    # Downgrade activity
    # ---------------------------------------------------------------

    if "downgrade_count" in df.columns:

        df["has_downgrade"] = (
            df["downgrade_count"] > 0
        ).astype(int)

    # ---------------------------------------------------------------
    # Expansion / contraction indicator
    # ---------------------------------------------------------------

    if {
        "upgrade_count",
        "downgrade_count",
    }.issubset(df.columns):

        df["upgrade_minus_downgrade"] = (
            df["upgrade_count"]
            - df["downgrade_count"]
        )

    # ---------------------------------------------------------------
    # Revenue tier
    # ---------------------------------------------------------------

    if "monthly_recurring_revenue" in df.columns:

        df["revenue_tier"] = pd.cut(
            df["monthly_recurring_revenue"],
            bins=[
                -np.inf,
                0,
                50,
                100,
                200,
                np.inf,
            ],
            labels=[
                "Free",
                "Low",
                "Medium",
                "High",
                "Premium",
            ],
        )

    return df


# =====================================================================
# CLEAN ML DATASET
# =====================================================================

def clean_feature_dataset(df):
    """
    Clean the final customer-level feature dataset.
    """

    df = df.copy()

    # ---------------------------------------------------------------
    # Remove duplicate customers
    # ---------------------------------------------------------------

    df = (
        df
        .drop_duplicates(
            subset=["user_id"]
        )
    )

    # ---------------------------------------------------------------
    # Replace infinite values
    # ---------------------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    # ---------------------------------------------------------------
    # Numeric missing values
    # ---------------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        if column == "churn":
            continue

        df[column] = (
            df[column]
            .fillna(0)
        )

    # ---------------------------------------------------------------
    # Categorical missing values
    # ---------------------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        df[column] = (
            df[column]
            .astype(str)
            .replace(
                {
                    "nan": "unknown",
                    "None": "unknown",
                }
            )
            .fillna("unknown")
        )

    return df


# =====================================================================
# FINALIZE CHURN TARGET
# =====================================================================

def finalize_target(
    features,
    original_df
):
    """
    Add churn target after all predictive features
    have been created.

    This keeps the target separate from the feature
    construction process.
    """

    target = (
        original_df[
            [
                "user_id",
                "churn",
            ]
        ]
        .drop_duplicates(
            subset=["user_id"]
        )
    )

    result = features.merge(
        target,
        on="user_id",
        how="left",
    )

    result["churn"] = (
        result["churn"]
        .fillna(0)
        .astype(int)
    )

    return result


# =====================================================================
# REMOVE LEAKAGE
# =====================================================================

def remove_leakage_columns(df):
    """
    Remove columns that directly reveal the churn outcome.

    These columns must never be used as predictive variables.
    """

    leakage_columns = [
        "subscription_end_date",
        "end_date",
        "churn_date",
        "cancellation_date",
        "status",
    ]

    columns_to_remove = [
        column
        for column in leakage_columns
        if column in df.columns
    ]

    if columns_to_remove:

        print(
            "\nRemoving leakage columns:"
        )

        for column in columns_to_remove:

            print(
                f"  - {column}"
            )

        df = df.drop(
            columns=columns_to_remove
        )

    return df


# =====================================================================
# SAVE FEATURES
# =====================================================================

def save_features(df):
    """
    Save final ML feature dataset.
    """

    ANALYTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        ANALYTICS_DIR
        / "churn_features.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nSaved:"
        f"\n{output_path}"
    )

    return output_path


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS CHURN FEATURE ENGINEERING")
    print("=" * 75)

    # ---------------------------------------------------------------
    # Load subscriptions
    # ---------------------------------------------------------------

    print(
        "\nLoading subscription data..."
    )

    subscriptions = load_subscriptions()

    # ---------------------------------------------------------------
    # Prepare
    # ---------------------------------------------------------------

    print(
        "\nPreparing subscription data..."
    )

    subscriptions = (
        prepare_subscriptions(
            subscriptions
        )
    )

    # ---------------------------------------------------------------
    # Target
    # ---------------------------------------------------------------

    print(
        "Creating churn target..."
    )

    subscriptions = (
        create_churn_target(
            subscriptions
        )
    )

    # ---------------------------------------------------------------
    # Subscription features
    # ---------------------------------------------------------------

    print(
        "\nCreating subscription features..."
    )

    features = (
        create_subscription_features(
            subscriptions
        )
    )

    print(
        f"Base features: "
        f"{features.shape}"
    )

    # ---------------------------------------------------------------
    # Revenue features
    # ---------------------------------------------------------------

    print(
        "\nLoading revenue features..."
    )

    revenue = load_revenue_features()

    features = create_revenue_features(
        features,
        revenue,
    )

    print(
        f"After revenue features: "
        f"{features.shape}"
    )

    # ---------------------------------------------------------------
    # Product features
    # ---------------------------------------------------------------

    print(
        "\nLoading product features..."
    )

    product_features = (
        load_product_features()
    )

    features = create_product_features(
        features,
        product_features,
    )

    print(
        f"After product features: "
        f"{features.shape}"
    )

    # ---------------------------------------------------------------
    # Derived features
    # ---------------------------------------------------------------

    print(
        "\nCreating derived features..."
    )

    features = (
        create_derived_features(
            features
        )
    )

    # ---------------------------------------------------------------
    # Clean
    # ---------------------------------------------------------------

    print(
        "Cleaning feature dataset..."
    )

    features = (
        clean_feature_dataset(
            features
        )
    )

    # ---------------------------------------------------------------
    # Target
    # ---------------------------------------------------------------

    print(
        "Adding churn target..."
    )

    features = finalize_target(
        features,
        subscriptions,
    )

    # ---------------------------------------------------------------
    # Leakage removal
    # ---------------------------------------------------------------

    print(
        "\nChecking for target leakage..."
    )

    features = remove_leakage_columns(
        features
    )

    # ---------------------------------------------------------------
    # Reorder user_id and churn
    # ---------------------------------------------------------------

    first_columns = [
        "user_id",
    ]

    if "churn" in features.columns:

        first_columns.append(
            "churn"
        )

    remaining_columns = [
        column
        for column in features.columns
        if column not in first_columns
    ]

    features = features[
        first_columns
        + remaining_columns
    ]

    # ---------------------------------------------------------------
    # Save
    # ---------------------------------------------------------------

    save_features(
        features
    )

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------

    print(
        "\n" + "=" * 75
    )

    print(
        "CHURN FEATURE DATASET SUMMARY"
    )

    print(
        "=" * 75
    )

    print(
        f"Rows: "
        f"{len(features):,}"
    )

    print(
        f"Columns: "
        f"{len(features.columns):,}"
    )

    print(
        f"Churned customers: "
        f"{features['churn'].sum():,}"
    )

    print(
        f"Retained customers: "
        f"{(features['churn'] == 0).sum():,}"
    )

    print(
        f"Churn rate: "
        f"{features['churn'].mean() * 100:.2f}%"
    )

    print(
        "\nFeature columns:"
    )

    for column in features.columns:

        print(
            f"  - {column}"
        )

    print(
        "\n" + "=" * 75
    )

    print(
        "CHURN FEATURE ENGINEERING COMPLETE"
    )

    print(
        "=" * 75
    )