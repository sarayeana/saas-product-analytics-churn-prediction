"""
Product analytics metrics for the SaaS Product Analytics &
Churn Prediction project.

This module calculates product usage and engagement KPIs from
the processed events dataset.

Main metrics
------------
    - DAU
    - WAU
    - MAU
    - DAU/MAU stickiness
    - Daily event volume
    - Events per active user
    - Session metrics
    - Feature adoption
    - Event-type usage
    - User engagement segments

Grain
-----
Daily metrics:
    One row = one calendar day

Feature metrics:
    One row = one feature

User engagement:
    One row = one user
"""

from pathlib import Path

from collections import Counter, deque

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


# -------------------------------------------------------------------
# Load Events
# -------------------------------------------------------------------

def load_events() -> pd.DataFrame:
    """
    Load the processed events dataset.

    Returns
    -------
    pd.DataFrame
        Processed events data.
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

    return events


# -------------------------------------------------------------------
# Daily Active Users
# -------------------------------------------------------------------

def calculate_dau(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate Daily Active Users.

    DAU =
        Number of unique users performing at least
        one event on a given day.

    Returns
    -------
    pd.DataFrame
        date, dau
    """

    dau = (
    events
    .groupby("event_date")["user_id"]
    .nunique()
    .reset_index(
        name="dau"
    )
    .rename(
        columns={
            "event_date": "date"
        }
    )
)

    return dau


# -------------------------------------------------------------------
# Weekly Active Users
# -------------------------------------------------------------------

def calculate_wau(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate rolling 7-day Weekly Active Users.

    A user is considered active in a given 7-day window if they
    performed at least one event during that window.

    Returns
    -------
    pd.DataFrame
        date, wau
    """

    active_days = (
        events[
            [
                "event_date",
                "user_id",
            ]
        ]
        .drop_duplicates()
        .sort_values("event_date")
    )

    daily_users = {
        date: set(group["user_id"])
        for date, group
        in active_days.groupby("event_date")
    }

    all_dates = pd.date_range(
        start=events["event_date"].min(),
        end=events["event_date"].max(),
        freq="D",
    )

    window_counter = Counter()

    window = deque()

    results = []

    for current_date in all_dates:

        current_users = daily_users.get(
            current_date,
            set(),
        )

        # Add today's users.
        for user_id in current_users:

            window_counter[user_id] += 1

        window.append(
            (
                current_date,
                current_users,
            )
        )

        # Remove users outside the 7-day window.
        while (
            window
            and (
                current_date
                - window[0][0]
            ).days >= 7
        ):

            _, old_users = window.popleft()

            for user_id in old_users:

                window_counter[user_id] -= 1

                if window_counter[user_id] <= 0:

                    del window_counter[user_id]

        results.append(
            {
                "date": current_date,
                "wau": len(window_counter),
            }
        )

    return pd.DataFrame(results)


# -------------------------------------------------------------------
# Monthly Active Users
# -------------------------------------------------------------------

def calculate_mau(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate rolling 30-day Monthly Active Users.

    MAU is based on a rolling 30-day window rather than
    calendar-month aggregation.

    Returns
    -------
    pd.DataFrame
        date, mau
    """

    active_days = (
        events[
            [
                "event_date",
                "user_id",
            ]
        ]
        .drop_duplicates()
        .sort_values("event_date")
    )

    daily_users = {
        date: set(group["user_id"])
        for date, group
        in active_days.groupby("event_date")
    }

    all_dates = pd.date_range(
        start=events["event_date"].min(),
        end=events["event_date"].max(),
        freq="D",
    )

    window_counter = Counter()

    window = deque()

    results = []

    for current_date in all_dates:

        current_users = daily_users.get(
            current_date,
            set(),
        )

        # Add today's users.
        for user_id in current_users:

            window_counter[user_id] += 1

        window.append(
            (
                current_date,
                current_users,
            )
        )

        # Remove users outside 30-day window.
        while (
            window
            and (
                current_date
                - window[0][0]
            ).days >= 30
        ):

            _, old_users = window.popleft()

            for user_id in old_users:

                window_counter[user_id] -= 1

                if window_counter[user_id] <= 0:

                    del window_counter[user_id]

        results.append(
            {
                "date": current_date,
                "mau": len(window_counter),
            }
        )

    return pd.DataFrame(results)


# -------------------------------------------------------------------
# Product Activity Summary
# -------------------------------------------------------------------

def create_daily_product_metrics(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create daily product usage metrics.

    Metrics include:

        - DAU
        - WAU
        - MAU
        - DAU/MAU stickiness
        - total events
        - sessions
        - average session duration
        - events per active user
    """

    dau = calculate_dau(
        events
    )

    wau = calculate_wau(
        events
    )

    mau = calculate_mau(
        events
    )

    metrics = dau.merge(
        wau,
        on="date",
        how="left",
    )

    metrics = metrics.merge(
        mau,
        on="date",
        how="left",
    )

    # ---------------------------------------------------------------
    # Daily event metrics
    # ---------------------------------------------------------------

    event_metrics = (
        events
        .groupby("event_date")
        .agg(
            total_events=(
                "event_id",
                "count",
            ),
            sessions=(
                "session_id",
                "nunique",
            ),
            avg_session_duration_minutes=(
                "session_duration_minutes",
                "mean",
            ),
            total_session_duration_minutes=(
                "session_duration_minutes",
                "sum",
            ),
        )
        .reset_index()
        .rename(
            columns={
                "event_date": "date"
            }
        )
    )

    metrics = metrics.merge(
        event_metrics,
        on="date",
        how="left",
    )

    # ---------------------------------------------------------------
    # Derived metrics
    # ---------------------------------------------------------------

    metrics["stickiness_dau_mau"] = np.where(
        metrics["mau"] > 0,
        (
            metrics["dau"]
            / metrics["mau"]
        ) * 100,
        0,
    )

    metrics["events_per_active_user"] = np.where(
        metrics["dau"] > 0,
        (
            metrics["total_events"]
            / metrics["dau"]
        ),
        0,
    )

    metrics["sessions_per_active_user"] = np.where(
        metrics["dau"] > 0,
        (
            metrics["sessions"]
            / metrics["dau"]
        ),
        0,
    )

    return metrics.sort_values(
        "date"
    )


# -------------------------------------------------------------------
# Feature Usage
# -------------------------------------------------------------------

def calculate_feature_usage(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate product feature usage.

    Metrics include:

        - total events
        - unique users
        - events per user
        - percentage of all events
    """

    total_events = len(events)

    feature_usage = (
        events
        .groupby("feature")
        .agg(
            total_events=(
                "event_id",
                "count",
            ),
            unique_users=(
                "user_id",
                "nunique",
            ),
            active_days=(
                "event_date",
                "nunique",
            ),
        )
        .reset_index()
    )

    feature_usage["events_per_user"] = np.where(
        feature_usage["unique_users"] > 0,
        (
            feature_usage["total_events"]
            / feature_usage["unique_users"]
        ),
        0,
    )

    feature_usage["event_share_pct"] = np.where(
        total_events > 0,
        (
            feature_usage["total_events"]
            / total_events
        ) * 100,
        0,
    )

    feature_usage = feature_usage.sort_values(
        "total_events",
        ascending=False,
    )

    return feature_usage


# -------------------------------------------------------------------
# Event Type Usage
# -------------------------------------------------------------------

def calculate_event_type_usage(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate usage by event type.
    """

    total_events = len(events)

    event_type_usage = (
        events
        .groupby("event_type")
        .agg(
            total_events=(
                "event_id",
                "count",
            ),
            unique_users=(
                "user_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    event_type_usage["event_share_pct"] = np.where(
        total_events > 0,
        (
            event_type_usage["total_events"]
            / total_events
        ) * 100,
        0,
    )

    event_type_usage["events_per_user"] = np.where(
        event_type_usage["unique_users"] > 0,
        (
            event_type_usage["total_events"]
            / event_type_usage["unique_users"]
        ),
        0,
    )

    return event_type_usage.sort_values(
        "total_events",
        ascending=False,
    )


# -------------------------------------------------------------------
# User Engagement
# -------------------------------------------------------------------

def calculate_user_engagement(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create user-level product engagement metrics.

    Features include:

        - total_events
        - active_days
        - session_count
        - unique_features
        - avg_session_duration
        - events_per_active_day
    """

    engagement = (
        events
        .groupby("user_id")
        .agg(
            total_events=(
                "event_id",
                "count",
            ),
            active_days=(
                "event_date",
                "nunique",
            ),
            session_count=(
                "session_id",
                "nunique",
            ),
            unique_features=(
                "feature",
                "nunique",
            ),
            unique_event_types=(
                "event_type",
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
            first_activity_date=(
                "event_date",
                "min",
            ),
            last_activity_date=(
                "event_date",
                "max",
            ),
        )
        .reset_index()
    )

    engagement["events_per_active_day"] = np.where(
        engagement["active_days"] > 0,
        (
            engagement["total_events"]
            / engagement["active_days"]
        ),
        0,
    )

    engagement["events_per_session"] = np.where(
        engagement["session_count"] > 0,
        (
            engagement["total_events"]
            / engagement["session_count"]
        ),
        0,
    )

    engagement["activity_span_days"] = (
        engagement["last_activity_date"]
        - engagement["first_activity_date"]
    ).dt.days

    return engagement


# -------------------------------------------------------------------
# Engagement Segmentation
# -------------------------------------------------------------------

def assign_engagement_segment(
    engagement: pd.DataFrame,
) -> pd.DataFrame:
    """
    Assign users to engagement segments.

    Segments are based on active days and total events.

    Categories:

        Power User
        Highly Engaged
        Moderately Engaged
        Low Engagement
        Inactive
    """

    df = engagement.copy()

    conditions = [
        (
            (df["active_days"] >= 60)
            & (df["total_events"] >= 300)
        ),
        (
            (df["active_days"] >= 30)
            & (df["total_events"] >= 100)
        ),
        (
            (df["active_days"] >= 15)
            & (df["total_events"] >= 50)
        ),
        (
            (df["active_days"] >= 5)
            & (df["total_events"] >= 10)
        ),
        (
            (df["active_days"] < 5)
            | (df["total_events"] < 10)
        ),
    ]

    choices = [
        "Power User",
        "Highly Engaged",
        "Moderately Engaged",
        "Low Engagement",
        "Inactive",
    ]

    df["engagement_segment"] = np.select(
        conditions,
        choices,
        default="Unclassified",
    )

    return df


# -------------------------------------------------------------------
# Feature Adoption Matrix
# -------------------------------------------------------------------

def create_feature_adoption_matrix(
    events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a user × feature adoption matrix.

    Values represent the number of events generated by each
    user for each feature.
    """

    matrix = pd.pivot_table(
        events,
        index="user_id",
        columns="feature",
        values="event_id",
        aggfunc="count",
        fill_value=0,
    )

    matrix = matrix.reset_index()

    return matrix


# -------------------------------------------------------------------
# Save Analytics Outputs
# -------------------------------------------------------------------

def save_product_metrics(
    daily_metrics: pd.DataFrame,
    feature_usage: pd.DataFrame,
    event_type_usage: pd.DataFrame,
    user_engagement: pd.DataFrame,
    feature_adoption_matrix: pd.DataFrame,
) -> None:
    """
    Save product analytics outputs.
    """

    ANALYTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    outputs = {
        "daily_product_metrics.csv": daily_metrics,
        "feature_usage.csv": feature_usage,
        "event_type_usage.csv": event_type_usage,
        "user_engagement.csv": user_engagement,
        "feature_adoption_matrix.csv": feature_adoption_matrix,
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
    print("SAAS PRODUCT ANALYTICS")
    print("=" * 75)

    print("\nLoading processed events...")

    events = load_events()

    print(
        f"Events loaded: {len(events):,}"
    )

    print(
        f"Date range: "
        f"{events['event_date'].min().date()} "
        f"to "
        f"{events['event_date'].max().date()}"
    )

    # ---------------------------------------------------------------
    # Daily Product Metrics
    # ---------------------------------------------------------------

    print("\nCalculating DAU / WAU / MAU...")

    daily_metrics = create_daily_product_metrics(
        events
    )

    # ---------------------------------------------------------------
    # Feature Usage
    # ---------------------------------------------------------------

    print("Calculating feature usage...")

    feature_usage = calculate_feature_usage(
        events
    )

    # ---------------------------------------------------------------
    # Event Type Usage
    # ---------------------------------------------------------------

    print("Calculating event-type usage...")

    event_type_usage = calculate_event_type_usage(
        events
    )

    # ---------------------------------------------------------------
    # User Engagement
    # ---------------------------------------------------------------

    print("Calculating user engagement...")

    user_engagement = calculate_user_engagement(
        events
    )

    user_engagement = assign_engagement_segment(
        user_engagement
    )

    # ---------------------------------------------------------------
    # Feature Adoption Matrix
    # ---------------------------------------------------------------

    print("Building feature adoption matrix...")

    feature_adoption_matrix = (
        create_feature_adoption_matrix(
            events
        )
    )

    # ---------------------------------------------------------------
    # Save
    # ---------------------------------------------------------------

    print("\nSaving product analytics outputs...")

    save_product_metrics(
        daily_metrics,
        feature_usage,
        event_type_usage,
        user_engagement,
        feature_adoption_matrix,
    )

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------

    print("\nProduct Analytics Summary")
    print("-" * 75)

    print(
        f"Average DAU: "
        f"{daily_metrics['dau'].mean():,.0f}"
    )

    print(
        f"Average WAU: "
        f"{daily_metrics['wau'].mean():,.0f}"
    )

    print(
        f"Average MAU: "
        f"{daily_metrics['mau'].mean():,.0f}"
    )

    print(
        f"Average DAU/MAU Stickiness: "
        f"{daily_metrics['stickiness_dau_mau'].mean():.2f}%"
    )

    print(
        f"Total Features: "
        f"{feature_usage['feature'].nunique():,}"
    )

    print(
        f"Total Active Users: "
        f"{user_engagement['user_id'].nunique():,}"
    )

    print("\nTop 10 Features")

    print(
        feature_usage[
            [
                "feature",
                "total_events",
                "unique_users",
                "event_share_pct",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nEngagement Segments")

    segment_summary = (
        user_engagement[
            "engagement_segment"
        ]
        .value_counts()
        .rename_axis("segment")
        .reset_index(
            name="users"
        )
    )

    segment_summary["percentage"] = (
        segment_summary["users"]
        / segment_summary["users"].sum()
        * 100
    )

    print(
        segment_summary.to_string(
            index=False
        )
    )

    print("\n" + "=" * 75)
    print("PRODUCT ANALYTICS COMPLETE")
    print("=" * 75)