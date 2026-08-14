"""
Data loading module for the SaaS Product Analytics & Churn Prediction project.

This module provides reusable functions for loading the four raw datasets:

    - users.csv
    - events.csv
    - subscriptions.csv
    - support_tickets.csv

The functions return Pandas DataFrames and do not perform business
transformations. Data cleaning and validation are handled separately.
"""

from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# -------------------------------------------------------------------
# Dataset Paths
# -------------------------------------------------------------------

USERS_PATH = RAW_DATA_DIR / "users.csv"
EVENTS_PATH = RAW_DATA_DIR / "events.csv"
SUBSCRIPTIONS_PATH = RAW_DATA_DIR / "subscriptions.csv"
SUPPORT_TICKETS_PATH = RAW_DATA_DIR / "support_tickets.csv"


# -------------------------------------------------------------------
# Generic CSV Loader
# -------------------------------------------------------------------

def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the specified CSV file does not exist.
    ValueError
        If the CSV file is empty.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError(
            f"Dataset is empty: {file_path}"
        )

    return df


# -------------------------------------------------------------------
# Individual Dataset Loaders
# -------------------------------------------------------------------

def load_users() -> pd.DataFrame:
    """
    Load the users dataset.

    Returns
    -------
    pd.DataFrame
        User profile data.
    """

    return load_csv(USERS_PATH)


def load_events() -> pd.DataFrame:
    """
    Load the product events dataset.

    Returns
    -------
    pd.DataFrame
        Product usage event data.
    """

    return load_csv(EVENTS_PATH)


def load_subscriptions() -> pd.DataFrame:
    """
    Load the subscriptions dataset.

    Returns
    -------
    pd.DataFrame
        Subscription and revenue data.
    """

    return load_csv(SUBSCRIPTIONS_PATH)


def load_support_tickets() -> pd.DataFrame:
    """
    Load the support tickets dataset.

    Returns
    -------
    pd.DataFrame
        Customer support ticket data.
    """

    return load_csv(SUPPORT_TICKETS_PATH)


# -------------------------------------------------------------------
# Load All Datasets
# -------------------------------------------------------------------

def load_all_data() -> dict[str, pd.DataFrame]:
    """
    Load all project datasets.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing all four datasets.

    Example
    -------
    >>> data = load_all_data()
    >>> users = data["users"]
    >>> events = data["events"]
    """

    return {
        "users": load_users(),
        "events": load_events(),
        "subscriptions": load_subscriptions(),
        "support_tickets": load_support_tickets(),
    }


# -------------------------------------------------------------------
# Dataset Summary
# -------------------------------------------------------------------

def get_dataset_summary(
    data: dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Create a high-level summary of loaded datasets.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Dictionary returned by load_all_data().

    Returns
    -------
    pd.DataFrame
        Summary containing dataset names, rows, columns,
        and missing-value counts.
    """

    summary = []

    for name, df in data.items():

        summary.append(
            {
                "dataset": name,
                "rows": df.shape[0],
                "columns": df.shape[1],
                "missing_values": int(df.isna().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum()),
            }
        )

    return pd.DataFrame(summary)


# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("SaaS Product Analytics & Churn Prediction")
    print("Data Loading Test")
    print("=" * 70)

    datasets = load_all_data()

    summary = get_dataset_summary(datasets)

    print("\nDataset Summary:")
    print(summary.to_string(index=False))

    print("\nData loading completed successfully.")