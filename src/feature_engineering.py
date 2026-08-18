"""
Feature engineering module for the SaaS Product Analytics &
Churn Prediction project.

Purpose
-------
Transform the processed SaaS datasets into a user-level analytical
feature table.

Grain
-----
One row = one user.

The resulting feature table combines information from:

    - users
    - events
    - subscriptions
    - support_tickets

These features will be used by:

    - Product Analytics
    - Customer Analytics
    - Retention Analysis
    - Revenue Analysis
    - Churn Analysis
    - Churn Prediction
"""

from pathlib import Path

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

FEATURES_DIR = PROJECT_ROOT / "data" / "features"


# -------------------------------------------------------------------
# Dataset Loading
# -------------------------------------------------------------------

def load_processed_data() -> dict[str, pd.DataFrame]:
    """
    Load all processed datasets.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing users, events, subscriptions,
        and support tickets.
    """

    datasets = {
        "users": "users.csv",
        "events": "events.csv",
        "subscriptions": "subscriptions.csv",
        "support_tickets": "support_tickets.csv",
    }

    data = {}

    for dataset_name, filename in datasets.items():

        file_path = PROCESSED_DATA_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Processed dataset not found: {file_path}"
            )

        data[dataset_name] = pd.read_csv(
            file_path
        )

    return data


# -------------------------------------------------------------------
# Date Preparation
# -------------------------------------------------------------------

def prepare_dates(
    data: dict[str, pd.DataFrame]
) -> dict[str, pd.DataFrame]:
    """
    Convert date columns into Pandas datetime format.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Processed datasets.

    Returns
    -------
    dict[str, pd.DataFrame]
        Datasets with datetime columns converted.
    """

    data = {
        name: df.copy()
        for name, df in data.items()
    }

    data["users"]["signup_date"] = pd.to_datetime(
        data["users"]["signup_date"],
        errors="coerce",
    )

    data["events"]["event_timestamp"] = pd.to_datetime(
        data["events"]["event_timestamp"],
        errors="coerce",
    )

    data["subscriptions"][
        "subscription_start_date"
    ] = pd.to_datetime(
        data["subscriptions"]["subscription_start_date"],
        errors="coerce",
    )

    data["subscriptions"][
        "subscription_end_date"
    ] = pd.to_datetime(
        data["subscriptions"]["subscription_end_date"],
        errors="coerce",
    )

    data["support_tickets"]["created_at"] = pd.to_datetime(
        data["support_tickets"]["created_at"],
        errors="coerce",
    )

    data["support_tickets"]["resolved_at"] = pd.to_datetime(
        data["support_tickets"]["resolved_at"],
        errors="coerce",
    )

    return data


# -------------------------------------------------------------------
# Reference Date
# -------------------------------------------------------------------

def get_analysis_date(
    data: dict[str, pd.DataFrame]
) -> pd.Timestamp:
    """
    Determine the latest meaningful date across the datasets.

    Using the latest observed event/ticket/subscription date gives
    us a consistent analytical reference point.

    Returns
    -------
    pd.Timestamp
        Analysis reference date.
    """

    dates = []

    events = data["events"]

    if not events.empty:
        dates.append(
            events["event_timestamp"].max()
        )

    tickets = data["support_tickets"]

    if not tickets.empty:
        dates.append(
            tickets["created_at"].max()
        )

    subscriptions = data["subscriptions"]

    if not subscriptions.empty:
        dates.append(
            subscriptions["subscription_start_date"].max()
        )

    dates = [
        date
        for date in dates
        if pd.notna(date)
    ]

    if not dates:
        raise ValueError(
            "Unable to determine analysis date."
        )

    return max(dates)


# -------------------------------------------------------------------
# User Base Features
# -------------------------------------------------------------------

def create_user_base(
    users: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create the base user-level feature table.

    Grain:
        One row per user.
    """

    columns = [
        "user_id",
        "company_id",
        "signup_date",
        "country",
        "industry",
        "company_size",
        "acquisition_channel",
        "plan",
        "role",
        "primary_device",
        "engagement_propensity",
        "onboarding_completed",
    ]

    available_columns = [
        column
        for column in columns
        if column in users.columns
    ]

    user_base = users[
        available_columns
    ].copy()

    user_base = user_base.drop_duplicates(
        subset=["user_id"]
    )

    return user_base


# -------------------------------------------------------------------
# User Tenure
# -------------------------------------------------------------------

def add_user_tenure(
    user_features: pd.DataFrame,
    analysis_date: pd.Timestamp,
) -> pd.DataFrame:
    """
    Calculate user tenure in days.
    """

    df = user_features.copy()

    df["user_tenure_days"] = (
        analysis_date - df["signup_date"]
    ).dt.days

    df["user_tenure_days"] = (
        df["user_tenure_days"]
        .clip(lower=0)
    )

    return df


# -------------------------------------------------------------------
# Event-Level Features
# -------------------------------------------------------------------

def create_event_features(
    events: pd.DataFrame,
    analysis_date: pd.Timestamp,
) -> pd.DataFrame:
    """
    Aggregate product usage events to the user level.

    Features include:

        - total_events
        - active_days
        - session_count
        - avg_session_duration
        - total_session_duration
        - unique_features_used
        - unique_event_types
        - events_last_7_days
        - events_last_30_days
        - events_last_90_days
        - active_days_last_30_days
        - last_activity_date
        - days_since_last_activity
    """

    events = events.copy()

    # ---------------------------------------------------------------
    # Basic event aggregations
    # ---------------------------------------------------------------

    event_features = (
        events
        .groupby("user_id")
        .agg(
            total_events=(
                "event_id",
                "count",
            ),
            active_days=(
                "event_timestamp",
                lambda x: x.dt.date.nunique(),
            ),
            session_count=(
                "session_id",
                "nunique",
            ),
            avg_session_duration=(
                "session_duration_minutes",
                "mean",
            ),
            total_session_duration=(
                "session_duration_minutes",
                "sum",
            ),
            unique_features_used=(
                "feature",
                "nunique",
            ),
            unique_event_types=(
                "event_type",
                "nunique",
            ),
            last_activity_date=(
                "event_timestamp",
                "max",
            ),
        )
        .reset_index()
    )

    # ---------------------------------------------------------------
    # Time-window features
    # ---------------------------------------------------------------

    days_since_event = (
        analysis_date
        - events["event_timestamp"]
    ).dt.days

    events = events.assign(
        days_since_event=days_since_event
    )

    last_7 = (
        events["days_since_event"]
        .between(0, 6)
    )

    last_30 = (
        events["days_since_event"]
        .between(0, 29)
    )

    last_90 = (
        events["days_since_event"]
        .between(0, 89)
    )

    events_last_7 = (
        events.loc[last_7]
        .groupby("user_id")
        .size()
        .rename("events_last_7_days")
    )

    events_last_30 = (
        events.loc[last_30]
        .groupby("user_id")
        .size()
        .rename("events_last_30_days")
    )

    events_last_90 = (
        events.loc[last_90]
        .groupby("user_id")
        .size()
        .rename("events_last_90_days")
    )

    active_days_last_30 = (
        events.loc[last_30]
        .groupby("user_id")[
            "event_timestamp"
        ]
        .apply(
            lambda x: x.dt.date.nunique()
        )
        .rename("active_days_last_30_days")
    )

    # ---------------------------------------------------------------
    # Merge time-window features
    # ---------------------------------------------------------------

    event_features = event_features.merge(
        events_last_7,
        on="user_id",
        how="left",
    )

    event_features = event_features.merge(
        events_last_30,
        on="user_id",
        how="left",
    )

    event_features = event_features.merge(
        events_last_90,
        on="user_id",
        how="left",
    )

    event_features = event_features.merge(
        active_days_last_30,
        on="user_id",
        how="left",
    )

    # ---------------------------------------------------------------
    # Recency
    # ---------------------------------------------------------------

    event_features["days_since_last_activity"] = (
        analysis_date
        - event_features["last_activity_date"]
    ).dt.days

    return event_features


# -------------------------------------------------------------------
# Feature Adoption
# -------------------------------------------------------------------

def create_feature_adoption_features(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate product feature adoption metrics.

    Features:

        - unique_features_used
        - feature_adoption_rate

    Feature adoption rate is calculated as:

        unique features used
        --------------------
        total available features
    """

    total_features = events[
        "feature"
    ].nunique()

    adoption = (
        events
        .groupby("user_id")["feature"]
        .nunique()
        .reset_index(
            name="unique_features_used"
        )
    )

    if total_features > 0:

        adoption["feature_adoption_rate"] = (
            adoption["unique_features_used"]
            / total_features
        )

    else:

        adoption["feature_adoption_rate"] = 0.0

    return adoption


# -------------------------------------------------------------------
# Subscription Features
# -------------------------------------------------------------------

def create_subscription_features(
    subscriptions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate subscription information to the user level.

    Features include:

        - subscription_count
        - current_plan
        - current_subscription_status
        - billing_frequency
        - monthly_recurring_revenue
        - annual_contract_value
        - upgrade_count
        - downgrade_count
        - subscription_tenure_days
        - trial_user
    """

    subscriptions = subscriptions.copy()

    # Sort so the latest subscription record is last.
    subscriptions = subscriptions.sort_values(
        [
            "user_id",
            "subscription_start_date",
        ]
    )

    # Latest subscription for each user.
    latest_subscription = (
        subscriptions
        .drop_duplicates(
            subset=["user_id"],
            keep="last",
        )
        [
            [
                "user_id",
                "plan",
                "status",
                "billing_frequency",
                "trial",
            ]
        ]
        .rename(
            columns={
                "plan": "current_plan",
                "status": "current_subscription_status",
                "billing_frequency": "current_billing_frequency",
                "trial": "trial_user",
            }
        )
    )

    # Aggregated subscription metrics.
    subscription_metrics = (
        subscriptions
        .groupby("user_id")
        .agg(
            subscription_count=(
                "subscription_id",
                "nunique",
            ),
            monthly_recurring_revenue=(
                "monthly_recurring_revenue",
                "max",
            ),
            annual_contract_value=(
                "annual_contract_value",
                "max",
            ),
            total_upgrade_count=(
                "upgrade_count",
                "sum",
            ),
            total_downgrade_count=(
                "downgrade_count",
                "sum",
            ),
            subscription_tenure_days=(
                "tenure_days",
                "max",
            ),
        )
        .reset_index()
    )

    subscription_features = subscription_metrics.merge(
        latest_subscription,
        on="user_id",
        how="left",
    )

    return subscription_features


# -------------------------------------------------------------------
# Support Features
# -------------------------------------------------------------------

def create_support_features(
    support_tickets: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate support ticket information to the user level.

    Features include:

        - ticket_count
        - resolved_ticket_count
        - reopened_ticket_count
        - avg_resolution_time_hours
        - avg_satisfaction_score
        - high_priority_ticket_count
    """

    tickets = support_tickets.copy()

    support_features = (
        tickets
        .groupby("user_id")
        .agg(
            ticket_count=(
                "ticket_id",
                "nunique",
            ),
            resolved_ticket_count=(
                "resolved_at",
                lambda x: x.notna().sum(),
            ),
            reopened_ticket_count=(
                "reopened",
                "sum",
            ),
            avg_resolution_time_hours=(
                "resolution_time_hours",
                "mean",
            ),
            avg_satisfaction_score=(
                "satisfaction_score",
                "mean",
            ),
            high_priority_ticket_count=(
                "priority",
                lambda x: (
                    x.astype("string")
                    .str.lower()
                    .eq("high")
                    .sum()
                ),
            ),
        )
        .reset_index()
    )

    return support_features


# -------------------------------------------------------------------
# Engagement Features
# -------------------------------------------------------------------

def create_engagement_features(
    user_features: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create derived engagement metrics.
    """

    df = user_features.copy()

    # ---------------------------------------------------------------
    # Events per active day
    # ---------------------------------------------------------------

    df["events_per_active_day"] = np.where(
        df["active_days"] > 0,
        df["total_events"]
        / df["active_days"],
        0,
    )

    # ---------------------------------------------------------------
    # Events per session
    # ---------------------------------------------------------------

    df["events_per_session"] = np.where(
        df["session_count"] > 0,
        df["total_events"]
        / df["session_count"],
        0,
    )

    # ---------------------------------------------------------------
    # Recent activity ratio
    # ---------------------------------------------------------------

    df["recent_activity_ratio"] = np.where(
        df["total_events"] > 0,
        df["events_last_30_days"]
        / df["total_events"],
        0,
    )

    # ---------------------------------------------------------------
    # Support ticket rate
    # ---------------------------------------------------------------

    df["tickets_per_100_events"] = np.where(
        df["total_events"] > 0,
        (
            df["ticket_count"]
            / df["total_events"]
        ) * 100,
        0,
    )

    return df


# -------------------------------------------------------------------
# Default Values
# -------------------------------------------------------------------

def fill_feature_defaults(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Fill missing values created by left joins.

    Users without events, subscriptions, or tickets are retained.
    Their aggregated metrics are therefore set to appropriate
    zero/default values.
    """

    df = df.copy()

    zero_columns = [
        "total_events",
        "active_days",
        "session_count",
        "avg_session_duration",
        "total_session_duration",
        "unique_features_used",
        "unique_event_types",
        "events_last_7_days",
        "events_last_30_days",
        "events_last_90_days",
        "active_days_last_30_days",
        "days_since_last_activity",
        "feature_adoption_rate",
        "subscription_count",
        "monthly_recurring_revenue",
        "annual_contract_value",
        "total_upgrade_count",
        "total_downgrade_count",
        "subscription_tenure_days",
        "ticket_count",
        "resolved_ticket_count",
        "reopened_ticket_count",
        "avg_resolution_time_hours",
        "avg_satisfaction_score",
        "high_priority_ticket_count",
    ]

    for column in zero_columns:

        if column in df.columns:

            df[column] = df[column].fillna(0)

    # ---------------------------------------------------------------
    # Boolean defaults
    # ---------------------------------------------------------------

    if "trial_user" in df.columns:

        df["trial_user"] = (
            df["trial_user"]
            .fillna(False)
            .astype(bool)
        )

    if "onboarding_completed" in df.columns:

        df["onboarding_completed"] = (
            df["onboarding_completed"]
            .fillna(False)
            .astype(bool)
        )

    # ---------------------------------------------------------------
    # Text defaults
    # ---------------------------------------------------------------

    text_defaults = {
        "current_plan": "Unknown",
        "current_subscription_status": "Unknown",
        "current_billing_frequency": "Unknown",
    }

    for column, default in text_defaults.items():

        if column in df.columns:

            df[column] = df[column].fillna(
                default
            )

    return df


# -------------------------------------------------------------------
# Build User Feature Table
# -------------------------------------------------------------------

def build_user_feature_table(
    data: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Build the complete user-level feature table.

    Grain:
        One row per user.

    Returns
    -------
    pd.DataFrame
        User-level analytical feature table.
    """

    data = prepare_dates(data)

    analysis_date = get_analysis_date(data)

    # ---------------------------------------------------------------
    # Base
    # ---------------------------------------------------------------

    user_features = create_user_base(
        data["users"]
    )

    user_features = add_user_tenure(
        user_features,
        analysis_date,
    )

    # ---------------------------------------------------------------
    # Events
    # ---------------------------------------------------------------

    event_features = create_event_features(
        data["events"],
        analysis_date,
    )

    user_features = user_features.merge(
        event_features,
        on="user_id",
        how="left",
    )

    # ---------------------------------------------------------------
    # Feature Adoption
    # ---------------------------------------------------------------

    adoption_features = (
        create_feature_adoption_features(
            data["events"]
        )
    )

    user_features = user_features.merge(
        adoption_features,
        on="user_id",
        how="left",
        suffixes=("", "_adoption"),
    )

    # ---------------------------------------------------------------
    # Subscriptions
    # ---------------------------------------------------------------

    subscription_features = (
        create_subscription_features(
            data["subscriptions"]
        )
    )

    user_features = user_features.merge(
        subscription_features,
        on="user_id",
        how="left",
    )

    # ---------------------------------------------------------------
    # Support
    # ---------------------------------------------------------------

    support_features = (
        create_support_features(
            data["support_tickets"]
        )
    )

    user_features = user_features.merge(
        support_features,
        on="user_id",
        how="left",
    )

    # ---------------------------------------------------------------
    # Derived engagement metrics
    # ---------------------------------------------------------------

    user_features = create_engagement_features(
        user_features
    )

    # ---------------------------------------------------------------
    # Fill missing aggregate values
    # ---------------------------------------------------------------

    user_features = fill_feature_defaults(
        user_features
    )

    # ---------------------------------------------------------------
    # Add analysis metadata
    # ---------------------------------------------------------------

    user_features["analysis_date"] = analysis_date

    # ---------------------------------------------------------------
    # Remove accidental duplicate columns
    # ---------------------------------------------------------------

    if (
        "unique_features_used_adoption"
        in user_features.columns
    ):

        user_features = user_features.drop(
            columns=[
                "unique_features_used_adoption"
            ]
        )

    # ---------------------------------------------------------------
    # Final duplicate check
    # ---------------------------------------------------------------

    user_features = user_features.drop_duplicates(
        subset=["user_id"]
    )

    return user_features


# -------------------------------------------------------------------
# Save Feature Table
# -------------------------------------------------------------------

def save_user_feature_table(
    user_features: pd.DataFrame,
) -> Path:
    """
    Save the user-level feature table.

    Returns
    -------
    Path
        Output file path.
    """

    FEATURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        FEATURES_DIR
        / "user_features.csv"
    )

    user_features.to_csv(
        output_path,
        index=False,
    )

    return output_path


# -------------------------------------------------------------------
# Feature Summary
# -------------------------------------------------------------------

def get_feature_summary(
    user_features: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a summary of the generated feature table.
    """

    summary = pd.DataFrame(
        {
            "metric": [
                "rows",
                "columns",
                "missing_values",
                "duplicate_user_ids",
            ],
            "value": [
                len(user_features),
                len(user_features.columns),
                int(
                    user_features.isna()
                    .sum()
                    .sum()
                ),
                int(
                    user_features["user_id"]
                    .duplicated()
                    .sum()
                ),
            ],
        }
    )

    return summary


# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS USER-LEVEL FEATURE ENGINEERING")
    print("=" * 75)

    print("\nLoading processed datasets...")

    data = load_processed_data()

    print("Processed datasets loaded.")

    print("\nBuilding user-level feature table...")

    user_features = build_user_feature_table(
        data
    )

    print(
        f"Feature table created: "
        f"{user_features.shape[0]:,} users × "
        f"{user_features.shape[1]:,} features"
    )

    print("\nFeature Summary:")

    summary = get_feature_summary(
        user_features
    )

    print(
        summary.to_string(index=False)
    )

    print("\nSample Features:")

    preview_columns = [
        "user_id",
        "total_events",
        "active_days",
        "session_count",
        "events_last_7_days",
        "events_last_30_days",
        "unique_features_used",
        "feature_adoption_rate",
        "monthly_recurring_revenue",
        "ticket_count",
        "avg_satisfaction_score",
        "days_since_last_activity",
    ]

    available_preview_columns = [
        column
        for column in preview_columns
        if column in user_features.columns
    ]

    print(
        user_features[
            available_preview_columns
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nSaving feature table...")

    output_path = save_user_feature_table(
        user_features
    )

    print(
        f"Saved: {output_path}"
    )

    print("\n" + "=" * 75)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 75)