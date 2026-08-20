"""
Retention analytics module for the SaaS Product Analytics &
Churn Prediction project.

Purpose
-------
Analyze customer retention and user lifecycle behavior.

Main analyses
-------------
    - New users
    - Returning users
    - Monthly active users
    - Monthly retention
    - Cohort assignment
    - Cohort retention
    - Retention curves
    - User lifecycle metrics

Grain
-----
Daily metrics:
    One row = one day

Monthly metrics:
    One row = one month

Cohort retention:
    One row = one cohort/month combination
"""

from pathlib import Path

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = (
    PROJECT_ROOT / "data" / "processed"
)

ANALYTICS_DIR = (
    PROJECT_ROOT / "data" / "analytics"
)


# -------------------------------------------------------------------
# Load Users
# -------------------------------------------------------------------

def load_users() -> pd.DataFrame:
    """
    Load the processed users dataset.
    """

    file_path = (
        PROCESSED_DATA_DIR
        / "users.csv"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Processed users dataset not found: "
            f"{file_path}\n"
            f"Run preprocessing.py first."
        )

    users = pd.read_csv(
        file_path
    )

    users["signup_date"] = pd.to_datetime(
        users["signup_date"],
        errors="coerce",
    )

    users = users.dropna(
        subset=[
            "user_id",
            "signup_date",
        ]
    )

    return users


# -------------------------------------------------------------------
# Load Events
# -------------------------------------------------------------------

def load_events() -> pd.DataFrame:
    """
    Load the processed events dataset.
    """

    file_path = (
        PROCESSED_DATA_DIR
        / "events.csv"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Processed events dataset not found: "
            f"{file_path}\n"
            f"Run preprocessing.py first."
        )

    events = pd.read_csv(
        file_path
    )

    events["event_timestamp"] = pd.to_datetime(
        events["event_timestamp"],
        errors="coerce",
    )

    events = events.dropna(
        subset=[
            "user_id",
            "event_timestamp",
        ]
    )

    events["event_date"] = (
        events["event_timestamp"]
        .dt.normalize()
    )

    events["month"] = (
        events["event_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    return events


# -------------------------------------------------------------------
# Daily User Activity
# -------------------------------------------------------------------

def create_daily_user_activity(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create one row per active user per day.

    This removes multiple events from the same user on the same
    day and gives us the fundamental retention activity table.
    """

    daily_activity = (
        events[
            [
                "user_id",
                "event_date",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "user_id",
                "event_date",
            ]
        )
        .reset_index(drop=True)
    )

    return daily_activity


# -------------------------------------------------------------------
# Monthly User Activity
# -------------------------------------------------------------------

def create_monthly_user_activity(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create one row per active user per month.
    """

    monthly_activity = (
        events[
            [
                "user_id",
                "month",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "user_id",
                "month",
            ]
        )
        .reset_index(drop=True)
    )

    return monthly_activity


# -------------------------------------------------------------------
# New User Analysis
# -------------------------------------------------------------------

def calculate_new_users(
    users: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate new user signups by month.
    """

    users = users.copy()

    users["signup_month"] = (
        users["signup_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    new_users = (
        users
        .groupby("signup_month")
        .agg(
            new_users=(
                "user_id",
                "nunique",
            )
        )
        .reset_index()
        .rename(
            columns={
                "signup_month": "month"
            }
        )
    )

    return new_users.sort_values(
        "month"
    )


# -------------------------------------------------------------------
# Returning Users
# -------------------------------------------------------------------

def calculate_returning_users(
    monthly_activity: pd.DataFrame,
    users: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate new vs returning users by month.

    A user is considered:

        New:
            Active in the same month as signup.

        Returning:
            Active after their signup month.
    """

    user_signup = (
        users[
            [
                "user_id",
                "signup_date",
            ]
        ]
        .copy()
    )

    user_signup["signup_month"] = (
        user_signup["signup_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    activity = monthly_activity.merge(
        user_signup[
            [
                "user_id",
                "signup_month",
            ]
        ],
        on="user_id",
        how="left",
    )

    activity["user_type"] = np.where(
        activity["month"]
        == activity["signup_month"],
        "New",
        "Returning",
    )

    monthly_summary = (
        activity
        .groupby(
            [
                "month",
                "user_type",
            ]
        )
        .agg(
            users=(
                "user_id",
                "nunique",
            )
        )
        .reset_index()
    )

    return monthly_summary.sort_values(
        [
            "month",
            "user_type",
        ]
    )


# -------------------------------------------------------------------
# Monthly Active Users
# -------------------------------------------------------------------

def calculate_monthly_active_users(
    monthly_activity: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate monthly active users.
    """

    mau = (
        monthly_activity
        .groupby("month")
        .agg(
            monthly_active_users=(
                "user_id",
                "nunique",
            )
        )
        .reset_index()
    )

    return mau.sort_values(
        "month"
    )


# -------------------------------------------------------------------
# User Cohort Assignment
# -------------------------------------------------------------------

def assign_user_cohorts(
    users: pd.DataFrame,
) -> pd.DataFrame:
    """
    Assign each user to their signup cohort month.

    Example:

        signup_date = 2025-03-14

        cohort_month = 2025-03-01
    """

    cohort_users = users[
        [
            "user_id",
            "signup_date",
        ]
    ].copy()

    cohort_users["cohort_month"] = (
        cohort_users["signup_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    return cohort_users[
        [
            "user_id",
            "cohort_month",
        ]
    ]


# -------------------------------------------------------------------
# Cohort Activity
# -------------------------------------------------------------------

def create_cohort_activity(
    monthly_activity: pd.DataFrame,
    cohort_users: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine monthly user activity with cohort information.
    """

    activity = monthly_activity.merge(
        cohort_users,
        on="user_id",
        how="left",
    )

    activity["months_since_signup"] = (
        (
            activity["month"].dt.year
            - activity["cohort_month"].dt.year
        ) * 12
        +
        (
            activity["month"].dt.month
            - activity["cohort_month"].dt.month
        )
    )

    return activity


# -------------------------------------------------------------------
# Cohort Retention
# -------------------------------------------------------------------

def calculate_cohort_retention(
    cohort_activity: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate cohort retention.

    For each signup cohort:

        Month 0 = users active during signup month

        Month 1 = users active one month later

        Month 2 = users active two months later

        etc.

    Retention rate:

        Active users in period N
        ------------------------
        Cohort size at Month 0
    """

    cohort_sizes = (
        cohort_activity[
            cohort_activity["months_since_signup"] == 0
        ]
        .groupby("cohort_month")["user_id"]
        .nunique()
        .rename("cohort_size")
    )

    retention = (
        cohort_activity
        .groupby(
            [
                "cohort_month",
                "months_since_signup",
            ]
        )
        .agg(
            active_users=(
                "user_id",
                "nunique",
            )
        )
        .reset_index()
    )

    retention = retention.merge(
        cohort_sizes,
        on="cohort_month",
        how="left",
    )

    retention["retention_rate"] = np.where(
        retention["cohort_size"] > 0,
        (
            retention["active_users"]
            / retention["cohort_size"]
        ) * 100,
        0,
    )

    return retention.sort_values(
        [
            "cohort_month",
            "months_since_signup",
        ]
    )


# -------------------------------------------------------------------
# Retention Matrix
# -------------------------------------------------------------------

def create_retention_matrix(
    cohort_retention: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert cohort retention into a matrix.

    Rows:
        Signup cohort

    Columns:
        Month 0, Month 1, Month 2, ...

    Values:
        Retention percentage
    """

    matrix = pd.pivot_table(
        cohort_retention,
        index="cohort_month",
        columns="months_since_signup",
        values="retention_rate",
        aggfunc="mean",
    )

    matrix.columns = [
        f"Month_{int(column)}"
        for column in matrix.columns
    ]

    matrix = matrix.reset_index()

    return matrix


# -------------------------------------------------------------------
# Overall Retention
# -------------------------------------------------------------------

def calculate_overall_retention(
    cohort_retention: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate average retention by lifecycle month.

    This provides the overall retention curve.
    """

    overall = (
        cohort_retention
        .groupby("months_since_signup")
        .agg(
            average_retention_rate=(
                "retention_rate",
                "mean",
            ),
            median_retention_rate=(
                "retention_rate",
                "median",
            ),
            cohorts_available=(
                "cohort_month",
                "nunique",
            ),
        )
        .reset_index()
    )

    return overall.sort_values(
        "months_since_signup"
    )


# -------------------------------------------------------------------
# User Lifecycle Metrics
# -------------------------------------------------------------------

def calculate_user_lifecycle(
    users: pd.DataFrame,
    monthly_activity: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate lifecycle metrics for each user.

    Metrics:

        - first_active_month
        - last_active_month
        - active_months
        - lifecycle_months
        - activity_frequency
    """

    activity_summary = (
        monthly_activity
        .groupby("user_id")
        .agg(
            first_active_month=(
                "month",
                "min",
            ),
            last_active_month=(
                "month",
                "max",
            ),
            active_months=(
                "month",
                "nunique",
            ),
        )
        .reset_index()
    )

    lifecycle = users[
        [
            "user_id",
            "signup_date",
        ]
    ].merge(
        activity_summary,
        on="user_id",
        how="left",
    )

    lifecycle["lifecycle_months"] = (
        (
            lifecycle["last_active_month"].dt.year
            - lifecycle["first_active_month"].dt.year
        ) * 12
        +
        (
            lifecycle["last_active_month"].dt.month
            - lifecycle["first_active_month"].dt.month
        )
        + 1
    )

    lifecycle["activity_frequency_pct"] = np.where(
        lifecycle["lifecycle_months"] > 0,
        (
            lifecycle["active_months"]
            / lifecycle["lifecycle_months"]
        ) * 100,
        0,
    )

    lifecycle["active_months"] = (
        lifecycle["active_months"]
        .fillna(0)
    )

    lifecycle["lifecycle_months"] = (
        lifecycle["lifecycle_months"]
        .fillna(0)
    )

    lifecycle["activity_frequency_pct"] = (
        lifecycle["activity_frequency_pct"]
        .fillna(0)
    )

    return lifecycle


# -------------------------------------------------------------------
# Retention Summary
# -------------------------------------------------------------------

def create_retention_summary(
    new_users: pd.DataFrame,
    mau: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine acquisition and activity metrics.

    Metrics:

        - new users
        - MAU
        - new user percentage of MAU
        - returning user percentage
    """

    summary = new_users.merge(
        mau,
        on="month",
        how="outer",
    )

    summary = summary.sort_values(
        "month"
    )

    summary["new_users"] = (
        summary["new_users"]
        .fillna(0)
    )

    summary["monthly_active_users"] = (
        summary["monthly_active_users"]
        .fillna(0)
    )

    summary["new_user_share_pct"] = np.where(
        summary["monthly_active_users"] > 0,
        (
            summary["new_users"]
            / summary["monthly_active_users"]
        ) * 100,
        0,
    )

    summary["returning_user_share_pct"] = (
        100
        - summary["new_user_share_pct"]
    )

    return summary


# -------------------------------------------------------------------
# Save Outputs
# -------------------------------------------------------------------

def save_retention_outputs(
    new_users: pd.DataFrame,
    returning_users: pd.DataFrame,
    mau: pd.DataFrame,
    cohort_retention: pd.DataFrame,
    retention_matrix: pd.DataFrame,
    overall_retention: pd.DataFrame,
    lifecycle: pd.DataFrame,
    retention_summary: pd.DataFrame,
) -> None:
    """
    Save all retention analytics outputs.
    """

    ANALYTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    outputs = {
        "new_users.csv": new_users,
        "new_vs_returning_users.csv": returning_users,
        "monthly_active_users.csv": mau,
        "cohort_retention.csv": cohort_retention,
        "retention_matrix.csv": retention_matrix,
        "overall_retention_curve.csv": overall_retention,
        "user_lifecycle.csv": lifecycle,
        "retention_summary.csv": retention_summary,
    }

    for filename, dataframe in outputs.items():

        output_path = (
            ANALYTICS_DIR
            / filename
        )

        dataframe.to_csv(
            output_path,
            index=False,
        )

        print(
            f"Saved: {output_path}"
        )


# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS RETENTION ANALYTICS")
    print("=" * 75)

    # ---------------------------------------------------------------
    # Load
    # ---------------------------------------------------------------

    print("\nLoading users...")

    users = load_users()

    print(
        f"Users loaded: {len(users):,}"
    )

    print("\nLoading events...")

    events = load_events()

    print(
        f"Events loaded: {len(events):,}"
    )

    # ---------------------------------------------------------------
    # Daily Activity
    # ---------------------------------------------------------------

    print("\nCreating daily user activity...")

    daily_activity = create_daily_user_activity(
        events
    )

    print(
        f"Daily activity records: "
        f"{len(daily_activity):,}"
    )

    # ---------------------------------------------------------------
    # Monthly Activity
    # ---------------------------------------------------------------

    print("Creating monthly user activity...")

    monthly_activity = create_monthly_user_activity(
        events
    )

    print(
        f"Monthly activity records: "
        f"{len(monthly_activity):,}"
    )

    # ---------------------------------------------------------------
    # New Users
    # ---------------------------------------------------------------

    print("Calculating new users...")

    new_users = calculate_new_users(
        users
    )

    # ---------------------------------------------------------------
    # Returning Users
    # ---------------------------------------------------------------

    print("Calculating new vs returning users...")

    returning_users = calculate_returning_users(
        monthly_activity,
        users,
    )

    # ---------------------------------------------------------------
    # MAU
    # ---------------------------------------------------------------

    print("Calculating monthly active users...")

    mau = calculate_monthly_active_users(
        monthly_activity
    )

    # ---------------------------------------------------------------
    # Cohorts
    # ---------------------------------------------------------------

    print("Assigning user cohorts...")

    cohort_users = assign_user_cohorts(
        users
    )

    print("Creating cohort activity...")

    cohort_activity = create_cohort_activity(
        monthly_activity,
        cohort_users,
    )

    # ---------------------------------------------------------------
    # Cohort Retention
    # ---------------------------------------------------------------

    print("Calculating cohort retention...")

    cohort_retention = calculate_cohort_retention(
        cohort_activity
    )

    print("Creating retention matrix...")

    retention_matrix = create_retention_matrix(
        cohort_retention
    )

    # ---------------------------------------------------------------
    # Overall Retention
    # ---------------------------------------------------------------

    print("Calculating overall retention curve...")

    overall_retention = calculate_overall_retention(
        cohort_retention
    )

    # ---------------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------------

    print("Calculating user lifecycle metrics...")

    lifecycle = calculate_user_lifecycle(
        users,
        monthly_activity,
    )

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------

    retention_summary = create_retention_summary(
        new_users,
        mau,
    )

    # ---------------------------------------------------------------
    # Save
    # ---------------------------------------------------------------

    print("\nSaving retention outputs...")

    save_retention_outputs(
        new_users,
        returning_users,
        mau,
        cohort_retention,
        retention_matrix,
        overall_retention,
        lifecycle,
        retention_summary,
    )

    # ---------------------------------------------------------------
    # Display Summary
    # ---------------------------------------------------------------

    print("\nRetention Summary")
    print("-" * 75)

    print(
        f"Total users: "
        f"{users['user_id'].nunique():,}"
    )

    print(
        f"Total active users: "
        f"{monthly_activity['user_id'].nunique():,}"
    )

    print(
        f"Number of signup cohorts: "
        f"{cohort_users['cohort_month'].nunique():,}"
    )

    print("\nLatest Monthly Metrics")

    print(
        retention_summary
        .tail(6)
        .to_string(index=False)
    )

    print("\nOverall Retention Curve")

    print(
        overall_retention
        .head(12)
        .to_string(index=False)
    )

    print("\n" + "=" * 75)
    print("RETENTION ANALYTICS COMPLETE")
    print("=" * 75)