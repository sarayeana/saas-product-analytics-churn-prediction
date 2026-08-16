"""
Data preprocessing module for the SaaS Product Analytics &
Churn Prediction project.

Responsibilities
---------------
This module prepares validated raw datasets for downstream analysis.

Main operations:

    - Convert date/time columns
    - Normalize categorical columns
    - Normalize boolean columns
    - Convert numeric columns
    - Handle missing values where appropriate
    - Standardize text values
    - Preserve raw data
    - Save processed datasets

Important
---------
This module does not perform analytical aggregations or machine learning
feature engineering. Those responsibilities belong to later modules.
"""

from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# -------------------------------------------------------------------
# Date Columns
# -------------------------------------------------------------------

DATE_COLUMNS = {
    "users": [
        "signup_date",
    ],
    "events": [
        "event_timestamp",
    ],
    "subscriptions": [
        "subscription_start_date",
        "subscription_end_date",
    ],
    "support_tickets": [
        "created_at",
        "resolved_at",
    ],
}


# -------------------------------------------------------------------
# Numeric Columns
# -------------------------------------------------------------------

NUMERIC_COLUMNS = {
    "users": [
        "engagement_propensity",
    ],
    "events": [
        "session_duration_minutes",
    ],
    "subscriptions": [
        "monthly_recurring_revenue",
        "annual_contract_value",
        "upgrade_count",
        "downgrade_count",
        "tenure_days",
    ],
    "support_tickets": [
        "resolution_time_hours",
        "satisfaction_score",
    ],
}


# -------------------------------------------------------------------
# Boolean Columns
# -------------------------------------------------------------------

BOOLEAN_COLUMNS = {
    "users": [
        "onboarding_completed",
    ],
    "subscriptions": [
        "trial",
    ],
    "support_tickets": [
        "reopened",
    ],
}


# -------------------------------------------------------------------
# Categorical Columns
# -------------------------------------------------------------------

CATEGORICAL_COLUMNS = {
    "users": [
        "country",
        "industry",
        "company_size",
        "acquisition_channel",
        "plan",
        "role",
        "primary_device",
    ],
    "events": [
        "event_type",
        "feature",
        "device",
    ],
    "subscriptions": [
        "plan",
        "billing_frequency",
        "status",
        "acquisition_source",
    ],
    "support_tickets": [
        "category",
        "priority",
        "channel",
        "status",
        "plan_at_ticket",
        "subscription_status_at_ticket",
    ],
}


# -------------------------------------------------------------------
# Generic Helpers
# -------------------------------------------------------------------

def normalize_text_column(
    series: pd.Series,
) -> pd.Series:
    """
    Normalize a text/categorical column.

    Operations
    ----------
    - Convert values to pandas string type.
    - Remove leading/trailing whitespace.
    - Collapse repeated spaces.

    Parameters
    ----------
    series : pd.Series
        Input column.

    Returns
    -------
    pd.Series
        Normalized text column.
    """

    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


def convert_boolean_column(
    series: pd.Series,
) -> pd.Series:
    """
    Convert common boolean representations to pandas BooleanDtype.

    Supported examples include:

        True / False
        true / false
        TRUE / FALSE
        1 / 0
        yes / no
        y / n

    Parameters
    ----------
    series : pd.Series
        Input column.

    Returns
    -------
    pd.Series
        Boolean column.
    """

    if pd.api.types.is_bool_dtype(series):
        return series.astype("boolean")

    normalized = (
        series.astype("string")
        .str.strip()
        .str.lower()
    )

    mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "yes": True,
        "no": False,
        "y": True,
        "n": False,
    }

    return normalized.map(mapping).astype("boolean")


# -------------------------------------------------------------------
# Date Processing
# -------------------------------------------------------------------

def process_dates(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Convert specified columns to datetime.

    Invalid date values are converted to NaT.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list[str]
        Date columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with processed dates.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    return df


# -------------------------------------------------------------------
# Numeric Processing
# -------------------------------------------------------------------

def process_numeric_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Convert specified columns to numeric.

    Invalid numeric values are converted to NaN.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list[str]
        Numeric columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with processed numeric columns.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    return df


# -------------------------------------------------------------------
# Boolean Processing
# -------------------------------------------------------------------

def process_boolean_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Convert specified columns to BooleanDtype.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list[str]
        Boolean columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with processed boolean columns.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = convert_boolean_column(
                df[column]
            )

    return df


# -------------------------------------------------------------------
# Categorical Processing
# -------------------------------------------------------------------

def process_categorical_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Normalize categorical columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list[str]
        Categorical columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with normalized categorical values.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = normalize_text_column(
                df[column]
            )

    return df


# -------------------------------------------------------------------
# User Dataset
# -------------------------------------------------------------------

def preprocess_users(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocess the users dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned users dataset.
    """

    df = df.copy()

    df = process_dates(
        df,
        DATE_COLUMNS["users"],
    )

    df = process_numeric_columns(
        df,
        NUMERIC_COLUMNS["users"],
    )

    df = process_boolean_columns(
        df,
        BOOLEAN_COLUMNS["users"],
    )

    df = process_categorical_columns(
        df,
        CATEGORICAL_COLUMNS["users"],
    )

    return df


# -------------------------------------------------------------------
# Events Dataset
# -------------------------------------------------------------------

def preprocess_events(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocess the events dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned events dataset.
    """

    df = df.copy()

    df = process_dates(
        df,
        DATE_COLUMNS["events"],
    )

    df = process_numeric_columns(
        df,
        NUMERIC_COLUMNS["events"],
    )

    df = process_categorical_columns(
        df,
        CATEGORICAL_COLUMNS["events"],
    )

    return df


# -------------------------------------------------------------------
# Subscriptions Dataset
# -------------------------------------------------------------------

def preprocess_subscriptions(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocess the subscriptions dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned subscriptions dataset.
    """

    df = df.copy()

    df = process_dates(
        df,
        DATE_COLUMNS["subscriptions"],
    )

    df = process_numeric_columns(
        df,
        NUMERIC_COLUMNS["subscriptions"],
    )

    df = process_boolean_columns(
        df,
        BOOLEAN_COLUMNS["subscriptions"],
    )

    df = process_categorical_columns(
        df,
        CATEGORICAL_COLUMNS["subscriptions"],
    )

    return df


# -------------------------------------------------------------------
# Support Tickets Dataset
# -------------------------------------------------------------------

def preprocess_support_tickets(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocess the support tickets dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned support ticket dataset.
    """

    df = df.copy()

    df = process_dates(
        df,
        DATE_COLUMNS["support_tickets"],
    )

    df = process_numeric_columns(
        df,
        NUMERIC_COLUMNS["support_tickets"],
    )

    df = process_boolean_columns(
        df,
        BOOLEAN_COLUMNS["support_tickets"],
    )

    df = process_categorical_columns(
        df,
        CATEGORICAL_COLUMNS["support_tickets"],
    )

    return df


# -------------------------------------------------------------------
# Process All Datasets
# -------------------------------------------------------------------

def preprocess_all_data(
    data: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """
    Preprocess all four datasets.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Dictionary containing raw datasets.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing processed datasets.
    """

    return {
        "users": preprocess_users(
            data["users"]
        ),
        "events": preprocess_events(
            data["events"]
        ),
        "subscriptions": preprocess_subscriptions(
            data["subscriptions"]
        ),
        "support_tickets": preprocess_support_tickets(
            data["support_tickets"]
        ),
    }


# -------------------------------------------------------------------
# Processed Data Saving
# -------------------------------------------------------------------

def save_processed_data(
    data: dict[str, pd.DataFrame],
) -> None:
    """
    Save processed datasets to data/processed/.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Dictionary containing processed datasets.
    """

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for dataset_name, df in data.items():

        output_path = (
            PROCESSED_DATA_DIR
            / f"{dataset_name}.csv"
        )

        df.to_csv(
            output_path,
            index=False,
        )

        print(
            f"Saved: {output_path}"
        )


# -------------------------------------------------------------------
# Processing Summary
# -------------------------------------------------------------------

def get_processing_summary(
    raw_data: dict[str, pd.DataFrame],
    processed_data: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Compare raw and processed datasets.

    Parameters
    ----------
    raw_data : dict[str, pd.DataFrame]
        Original datasets.

    processed_data : dict[str, pd.DataFrame]
        Processed datasets.

    Returns
    -------
    pd.DataFrame
        Processing summary.
    """

    summary = []

    for dataset_name in raw_data:

        raw_df = raw_data[dataset_name]
        processed_df = processed_data[dataset_name]

        summary.append(
            {
                "dataset": dataset_name,
                "raw_rows": raw_df.shape[0],
                "processed_rows": processed_df.shape[0],
                "raw_columns": raw_df.shape[1],
                "processed_columns": processed_df.shape[1],
                "raw_missing_values": int(
                    raw_df.isna().sum().sum()
                ),
                "processed_missing_values": int(
                    processed_df.isna().sum().sum()
                ),
            }
        )

    return pd.DataFrame(summary)


# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":

    # Import here so this module can also be imported independently.
    from data_loader import load_all_data

    print("=" * 75)
    print("SAAS DATA PREPROCESSING")
    print("=" * 75)

    print("\nLoading raw datasets...")

    raw_data = load_all_data()

    print("Raw datasets loaded successfully.")

    print("\nPreprocessing datasets...")

    processed_data = preprocess_all_data(
        raw_data
    )

    print("Preprocessing completed successfully.")

    print("\nProcessing Summary:")

    summary = get_processing_summary(
        raw_data,
        processed_data,
    )

    print(
        summary.to_string(index=False)
    )

    print("\nSaving processed datasets...")

    save_processed_data(
        processed_data
    )

    print("\n" + "=" * 75)
    print("PREPROCESSING COMPLETE")
    print("=" * 75)
