from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# NUMBER FORMATTING
# ============================================================

def format_number(
    value,
    decimals=0,
):
    """
    Format a numeric value with commas.

    Example:
        1234567 -> 1,234,567
    """

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:

        return f"{float(value):,.{decimals}f}"

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"


# ============================================================
# CURRENCY FORMATTING
# ============================================================

def format_currency(
    value,
    decimals=0,
    currency="$",
):
    """
    Format a numeric value as currency.

    Example:
        1234567 -> $1,234,567
    """

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:

        return (
            f"{currency}"
            f"{float(value):,.{decimals}f}"
        )

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"


# ============================================================
# PERCENTAGE FORMATTING
# ============================================================

def format_percentage(
    value,
    decimals=1,
):
    """
    Format a decimal percentage.

    Example:
        0.253 -> 25.3%
    """

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:

        return (
            f"{float(value) * 100:.{decimals}f}%"
        )

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"


def format_percentage_value(
    value,
    decimals=1,
):
    """
    Format a percentage that is already
    expressed as a percentage.

    Example:
        25.3 -> 25.3%
    """

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:

        return (
            f"{float(value):.{decimals}f}%"
        )

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"


# ============================================================
# LARGE NUMBER FORMATTING
# ============================================================

def format_compact_number(
    value,
    decimals=1,
):
    """
    Convert large numbers into compact notation.

    Examples:
        1200 -> 1.2K
        1500000 -> 1.5M
        2000000000 -> 2.0B
    """

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:

        value = float(value)

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"

    absolute_value = abs(value)

    if absolute_value >= 1_000_000_000:

        return (
            f"{value / 1_000_000_000:.{decimals}f}B"
        )

    if absolute_value >= 1_000_000:

        return (
            f"{value / 1_000_000:.{decimals}f}M"
        )

    if absolute_value >= 1_000:

        return (
            f"{value / 1_000:.{decimals}f}K"
        )

    return f"{value:.{decimals}f}"


# ============================================================
# MRR / ARR
# ============================================================

def mrr_to_arr(
    mrr,
):
    """
    Convert Monthly Recurring Revenue to
    Annual Recurring Revenue.
    """

    if mrr is None:
        return np.nan

    if pd.isna(mrr):
        return np.nan

    return float(mrr) * 12


def arr_to_mrr(
    arr,
):
    """
    Convert Annual Recurring Revenue to
    Monthly Recurring Revenue.
    """

    if arr is None:
        return np.nan

    if pd.isna(arr):
        return np.nan

    return float(arr) / 12


# ============================================================
# GROWTH CALCULATION
# ============================================================

def calculate_growth(
    current,
    previous,
):
    """
    Calculate percentage growth.

    Returns a decimal.

    Example:
        current = 110
        previous = 100

        result = 0.10
    """

    if (
        current is None
        or previous is None
    ):

        return np.nan

    if (
        pd.isna(current)
        or pd.isna(previous)
    ):

        return np.nan

    if previous == 0:

        return np.nan

    return (
        float(current)
        - float(previous)
    ) / float(previous)


# ============================================================
# SAFE DIVISION
# ============================================================

def safe_divide(
    numerator,
    denominator,
):
    """
    Safely divide two numbers.

    Returns NaN when denominator is zero.
    """

    if denominator in (
        0,
        None,
    ):

        return np.nan

    if (
        pd.isna(numerator)
        or pd.isna(denominator)
    ):

        return np.nan

    return numerator / denominator


# ============================================================
# DATE HELPERS
# ============================================================

def format_date(
    value,
    date_format="%Y-%m-%d",
):
    """
    Format a date value.
    """

    if value is None:
        return "N/A"

    try:

        date_value = pd.to_datetime(
            value
        )

        if pd.isna(date_value):

            return "N/A"

        return date_value.strftime(
            date_format
        )

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"


def format_month(
    value,
):
    """
    Format a date as YYYY-MM.
    """

    if value is None:
        return "N/A"

    try:

        date_value = pd.to_datetime(
            value
        )

        if pd.isna(date_value):

            return "N/A"

        return date_value.strftime(
            "%Y-%m"
        )

    except (
        ValueError,
        TypeError,
    ):

        return "N/A"


# ============================================================
# DATAFRAME DATE PREPARATION
# ============================================================

def ensure_datetime(
    df,
    column,
):
    """
    Convert a dataframe column to datetime
    if it exists.
    """

    if column not in df.columns:

        return df

    df = df.copy()

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce",
    )

    return df


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(
    df,
    candidates,
):
    """
    Find the first matching column from
    a list of candidates.
    """

    for column in candidates:

        if column in df.columns:

            return column

    return None


# ============================================================
# DATAFRAME SAFETY
# ============================================================

def is_valid_dataframe(
    df,
):
    """
    Check whether an object is a non-empty
    pandas DataFrame.
    """

    return (
        isinstance(
            df,
            pd.DataFrame,
        )
        and not df.empty
    )


# ============================================================
# UNIQUE VALUES
# ============================================================

def get_unique_values(
    df,
    column,
):
    """
    Return sorted unique values from a
    dataframe column.
    """

    if not is_valid_dataframe(df):

        return []

    if column not in df.columns:

        return []

    values = (
        df[column]
        .dropna()
        .unique()
        .tolist()
    )

    try:

        return sorted(values)

    except TypeError:

        return values


# ============================================================
# FILTER DATAFRAME
# ============================================================

def filter_by_value(
    df,
    column,
    value,
):
    """
    Filter a dataframe by one column value.
    """

    if not is_valid_dataframe(df):

        return pd.DataFrame()

    if column not in df.columns:

        return df.copy()

    return df[
        df[column] == value
    ].copy()


# ============================================================
# MULTI-FILTER DATAFRAME
# ============================================================

def apply_filters(
    df,
    filters,
):
    """
    Apply multiple equality filters.

    Example:

        filters = {
            "plan": "Professional",
            "risk_segment": "High",
        }
    """

    if not is_valid_dataframe(df):

        return pd.DataFrame()

    filtered_df = df.copy()

    for column, value in filters.items():

        if column not in filtered_df.columns:

            continue

        if value in (
            None,
            "All",
            "All Plans",
            "All Segments",
        ):

            continue

        if isinstance(
            value,
            list,
        ):

            filtered_df = filtered_df[
                filtered_df[column].isin(
                    value
                )
            ]

        else:

            filtered_df = filtered_df[
                filtered_df[column] == value
            ]

    return filtered_df


# ============================================================
# RISK LABEL
# ============================================================

def risk_label(
    probability,
):
    """
    Convert churn probability into
    a business-friendly risk segment.
    """

    if probability is None:

        return "Unknown"

    if pd.isna(probability):

        return "Unknown"

    probability = float(
        probability
    )

    if probability < 0.20:

        return "Very Low"

    if probability < 0.40:

        return "Low"

    if probability < 0.60:

        return "Medium"

    if probability < 0.80:

        return "High"

    return "Very High"


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def add_risk_segment(
    df,
    probability_column="churn_probability",
):
    """
    Add a risk segment column to a dataframe.
    """

    if not is_valid_dataframe(df):

        return df.copy()

    if probability_column not in df.columns:

        return df.copy()

    result = df.copy()

    result[
        "risk_segment"
    ] = result[
        probability_column
    ].apply(
        risk_label
    )

    return result


# ============================================================
# CHURN PRIORITY SCORE
# ============================================================

def calculate_risk_value(
    df,
    probability_column="churn_probability",
    revenue_column="monthly_recurring_revenue",
):
    """
    Calculate estimated revenue at risk.

    Risk Value =
        Churn Probability × MRR
    """

    if not is_valid_dataframe(df):

        return df.copy()

    if (
        probability_column
        not in df.columns
    ):

        return df.copy()

    if (
        revenue_column
        not in df.columns
    ):

        return df.copy()

    result = df.copy()

    result[
        "risk_value"
    ] = (
        result[
            probability_column
        ].fillna(0)
        *
        result[
            revenue_column
        ].fillna(0)
    )

    return result


# ============================================================
# TOP N
# ============================================================

def top_n(
    df,
    column,
    n=10,
    ascending=False,
):
    """
    Return top N records by a column.
    """

    if not is_valid_dataframe(df):

        return pd.DataFrame()

    if column not in df.columns:

        return df.head(n)

    return (
        df
        .sort_values(
            column,
            ascending=ascending,
        )
        .head(n)
        .copy()
    )


# ============================================================
# FILE EXISTENCE
# ============================================================

def file_exists(
    path,
):
    """
    Check whether a file exists.
    """

    return Path(
        path
    ).exists()


# ============================================================
# DATAFRAME COLUMN CHECK
# ============================================================

def has_columns(
    df,
    columns,
):
    """
    Check whether dataframe contains
    all requested columns.
    """

    if not isinstance(
        df,
        pd.DataFrame,
    ):

        return False

    return all(
        column in df.columns
        for column in columns
    )


# ============================================================
# EMPTY DATAFRAME MESSAGE
# ============================================================

def empty_message(
    dataframe_name,
):
    """
    Return a consistent message for
    unavailable dashboard data.
    """

    return (
        f"No data available for "
        f"{dataframe_name}."
    )