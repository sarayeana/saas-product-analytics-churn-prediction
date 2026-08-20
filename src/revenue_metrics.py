"""
SaaS Revenue Analytics
======================

Purpose
-------
Calculate SaaS subscription, revenue, and customer-value metrics.

Main metrics
------------
    - Monthly Recurring Revenue (MRR)
    - Annual Recurring Revenue (ARR)
    - Average Revenue Per User (ARPU)
    - Revenue by plan
    - Revenue by billing frequency
    - New subscriptions
    - Cancellations
    - Customer revenue
    - Revenue concentration
    - Revenue growth
    - Subscription trends

Dataset
-------
subscriptions.csv

Expected columns
----------------
    subscription_id
    user_id
    company_id
    plan
    subscription_start_date
    subscription_end_date
    billing_frequency
    monthly_recurring_revenue
    annual_contract_value
    trial
    status
    acquisition_source
    upgrade_count
    downgrade_count
    tenure_days
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ===================================================================
# PROJECT PATHS
# ===================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = (
    PROJECT_ROOT / "data" / "processed"
)

ANALYTICS_DIR = (
    PROJECT_ROOT / "data" / "analytics"
)


# ===================================================================
# LOAD SUBSCRIPTIONS
# ===================================================================

def load_subscriptions() -> pd.DataFrame:
    """
    Load processed subscriptions dataset.
    """

    file_path = (
        PROCESSED_DATA_DIR
        / "subscriptions.csv"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Processed subscriptions dataset not found:\n"
            f"{file_path}\n\n"
            f"Run preprocessing.py first."
        )

    subscriptions = pd.read_csv(
        file_path
    )

    print("\nSubscription columns detected:")

    print(
        subscriptions.columns.tolist()
    )

    return subscriptions


# ===================================================================
# STANDARDIZE SUBSCRIPTION COLUMNS
# ===================================================================

def standardize_subscription_columns(
    subscriptions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize the actual subscription dataset
    into analytical column names.

    Actual dataset:

        monthly_recurring_revenue
        billing_frequency
        subscription_start_date
        subscription_end_date

    Analytical names:

        price
        billing_cycle
        start_date
        end_date
    """

    df = subscriptions.copy()

    # ---------------------------------------------------------------
    # Required columns
    # ---------------------------------------------------------------

    required_columns = [
        "user_id",
        "plan",
        "subscription_start_date",
        "billing_frequency",
        "monthly_recurring_revenue",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise KeyError(
            "Required subscription columns are missing:\n"
            f"{missing_columns}\n\n"
            f"Available columns:\n"
            f"{df.columns.tolist()}"
        )

    # ---------------------------------------------------------------
    # Rename actual dataset columns
    # ---------------------------------------------------------------

    rename_map = {
        "monthly_recurring_revenue":
            "price",

        "billing_frequency":
            "billing_cycle",

        "subscription_start_date":
            "start_date",
    }

    if "subscription_end_date" in df.columns:

        rename_map[
            "subscription_end_date"
        ] = "end_date"

    df = df.rename(
        columns=rename_map
    )

    # ---------------------------------------------------------------
    # Convert data types
    # ---------------------------------------------------------------

    df["start_date"] = pd.to_datetime(
        df["start_date"],
        errors="coerce",
    )

    if "end_date" in df.columns:

        df["end_date"] = pd.to_datetime(
            df["end_date"],
            errors="coerce",
        )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce",
    )

    # ---------------------------------------------------------------
    # Clean text columns
    # ---------------------------------------------------------------

    df["plan"] = (
        df["plan"]
        .astype(str)
        .str.strip()
    )

    df["billing_cycle"] = (
        df["billing_cycle"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    if "status" in df.columns:

        df["status"] = (
            df["status"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

    # ---------------------------------------------------------------
    # Remove invalid records
    # ---------------------------------------------------------------

    df = df.dropna(
        subset=[
            "user_id",
            "start_date",
            "price",
        ]
    )

    # ---------------------------------------------------------------
    # Monthly revenue
    #
    # IMPORTANT:
    #
    # The dataset already contains
    # monthly_recurring_revenue.
    #
    # Therefore we DO NOT divide annual
    # subscriptions by 12.
    # ---------------------------------------------------------------

    df["monthly_revenue"] = df["price"]

    return df


# ===================================================================
# MONTHLY SUBSCRIPTION SNAPSHOT
# ===================================================================

def create_monthly_subscription_snapshot(
    subscriptions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a monthly snapshot of active subscriptions.

    A subscription is considered active in a month when:

        start_date <= month_end

    AND

        end_date is missing

    OR

        end_date >= month_start
    """

    df = subscriptions.copy()

    min_date = (
        df["start_date"]
        .min()
    )

    if "end_date" in df.columns:

        valid_end_dates = (
            df["end_date"]
            .dropna()
        )

        if not valid_end_dates.empty:

            max_date = max(
                valid_end_dates.max(),
                df["start_date"].max(),
            )

        else:

            max_date = (
                df["start_date"]
                .max()
            )

    else:

        max_date = (
            df["start_date"]
            .max()
        )

    if pd.isna(min_date) or pd.isna(max_date):

        return pd.DataFrame()

    start_month = (
        min_date
        .to_period("M")
        .start_time
    )

    end_month = (
        max_date
        .to_period("M")
        .start_time
    )

    months = pd.date_range(
        start=start_month,
        end=end_month,
        freq="MS",
    )

    snapshots = []

    for month in months:

        month_end = (
            month
            + pd.offsets.MonthEnd(0)
        )

        active = df[
            df["start_date"]
            <= month_end
        ].copy()

        if "end_date" in active.columns:

            active = active[
                active["end_date"].isna()
                |
                (
                    active["end_date"]
                    >= month
                )
            ]

        active["month"] = month

        snapshots.append(
            active
        )

    if not snapshots:

        return pd.DataFrame()

    snapshot = pd.concat(
        snapshots,
        ignore_index=True,
    )

    return snapshot


# ===================================================================
# MRR
# ===================================================================

def calculate_mrr(
    monthly_snapshot: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate Monthly Recurring Revenue.

    MRR
        = Sum of monthly recurring revenue
          from active subscriptions.
    """

    if monthly_snapshot.empty:

        return pd.DataFrame(
            columns=[
                "month",
                "mrr",
                "active_customers",
                "active_subscriptions",
            ]
        )

    mrr = (
        monthly_snapshot
        .groupby("month")
        .agg(
            mrr=(
                "monthly_revenue",
                "sum",
            ),
            active_customers=(
                "user_id",
                "nunique",
            ),
            active_subscriptions=(
                "subscription_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    return mrr.sort_values(
        "month"
    )


# ===================================================================
# ARR
# ===================================================================

def calculate_arr(
    mrr: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate Annual Recurring Revenue.

    ARR = MRR × 12
    """

    df = mrr.copy()

    df["arr"] = (
        df["mrr"] * 12
    )

    return df


# ===================================================================
# ARPU
# ===================================================================

def calculate_arpu(
    revenue_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate Average Revenue Per User.

    ARPU = MRR / Active Customers
    """

    df = revenue_metrics.copy()

    df["arpu"] = np.where(
        df["active_customers"] > 0,
        (
            df["mrr"]
            / df["active_customers"]
        ),
        0,
    )

    return df


# ===================================================================
# REVENUE GROWTH
# ===================================================================

def calculate_revenue_growth(
    revenue_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate month-over-month MRR growth.
    """

    df = revenue_metrics.copy()

    df["previous_mrr"] = (
        df["mrr"]
        .shift(1)
    )

    df["mrr_growth"] = (
        df["mrr"]
        - df["previous_mrr"]
    )

    df["mrr_growth_pct"] = np.where(
        df["previous_mrr"] > 0,
        (
            df["mrr_growth"]
            / df["previous_mrr"]
        ) * 100,
        np.nan,
    )

    return df


# ===================================================================
# REVENUE BY PLAN
# ===================================================================

def calculate_revenue_by_plan(
    monthly_snapshot: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate revenue and customers by subscription plan.
    """

    if monthly_snapshot.empty:

        return pd.DataFrame(
            columns=[
                "month",
                "plan",
                "mrr",
                "customers",
                "arpu",
            ]
        )

    plan_metrics = (
        monthly_snapshot
        .groupby(
            [
                "month",
                "plan",
            ]
        )
        .agg(
            mrr=(
                "monthly_revenue",
                "sum",
            ),
            customers=(
                "user_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    plan_metrics["arpu"] = np.where(
        plan_metrics["customers"] > 0,
        (
            plan_metrics["mrr"]
            / plan_metrics["customers"]
        ),
        0,
    )

    return plan_metrics.sort_values(
        [
            "month",
            "mrr",
        ],
        ascending=[
            True,
            False,
        ],
    )


# ===================================================================
# REVENUE BY BILLING FREQUENCY
# ===================================================================

def calculate_revenue_by_billing_cycle(
    monthly_snapshot: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate revenue by billing frequency.
    """

    if monthly_snapshot.empty:

        return pd.DataFrame(
            columns=[
                "month",
                "billing_cycle",
                "mrr",
                "customers",
            ]
        )

    cycle_metrics = (
        monthly_snapshot
        .groupby(
            [
                "month",
                "billing_cycle",
            ]
        )
        .agg(
            mrr=(
                "monthly_revenue",
                "sum",
            ),
            customers=(
                "user_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    return cycle_metrics.sort_values(
        [
            "month",
            "mrr",
        ],
        ascending=[
            True,
            False,
        ],
    )


# ===================================================================
# NEW SUBSCRIPTIONS
# ===================================================================

def calculate_new_subscriptions(
    subscriptions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate new subscriptions by month.
    """

    df = subscriptions.copy()

    df["month"] = (
        df["start_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    new_subscriptions = (
        df
        .groupby("month")
        .agg(
            new_subscriptions=(
                "subscription_id",
                "nunique",
            ),
            new_customers=(
                "user_id",
                "nunique",
            ),
            new_mrr=(
                "monthly_revenue",
                "sum",
            ),
        )
        .reset_index()
    )

    return new_subscriptions.sort_values(
        "month"
    )


# ===================================================================
# CANCELLATIONS
# ===================================================================

def calculate_cancellations(
    subscriptions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate cancellations by month.
    """

    if "end_date" not in subscriptions.columns:

        return pd.DataFrame(
            columns=[
                "month",
                "cancellations",
                "cancelled_customers",
                "lost_mrr",
            ]
        )

    df = subscriptions[
        subscriptions["end_date"].notna()
    ].copy()

    if df.empty:

        return pd.DataFrame(
            columns=[
                "month",
                "cancellations",
                "cancelled_customers",
                "lost_mrr",
            ]
        )

    df["month"] = (
        df["end_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    cancellations = (
        df
        .groupby("month")
        .agg(
            cancellations=(
                "subscription_id",
                "nunique",
            ),
            cancelled_customers=(
                "user_id",
                "nunique",
            ),
            lost_mrr=(
                "monthly_revenue",
                "sum",
            ),
        )
        .reset_index()
    )

    return cancellations.sort_values(
        "month"
    )


# ===================================================================
# CUSTOMER REVENUE
# ===================================================================

def calculate_customer_revenue(
    monthly_snapshot: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate customer-level recurring revenue.
    """

    if monthly_snapshot.empty:

        return pd.DataFrame(
            columns=[
                "user_id",
                "total_mrr",
                "average_monthly_revenue",
                "active_months",
                "plans_used",
                "estimated_annual_value",
            ]
        )

    customer_revenue = (
        monthly_snapshot
        .groupby("user_id")
        .agg(
            total_mrr=(
                "monthly_revenue",
                "sum",
            ),
            average_monthly_revenue=(
                "monthly_revenue",
                "mean",
            ),
            active_months=(
                "month",
                "nunique",
            ),
            plans_used=(
                "plan",
                "nunique",
            ),
        )
        .reset_index()
    )

    customer_revenue[
        "estimated_annual_value"
    ] = (
        customer_revenue[
            "average_monthly_revenue"
        ] * 12
    )

    return customer_revenue.sort_values(
        "total_mrr",
        ascending=False,
    )


# ===================================================================
# REVENUE CONCENTRATION
# ===================================================================

def calculate_revenue_concentration(
    customer_revenue: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate customer revenue concentration.

    This helps identify whether revenue is concentrated
    among a small number of customers.
    """

    df = customer_revenue.copy()

    if df.empty:

        return df

    total_revenue = (
        df["total_mrr"]
        .sum()
    )

    if total_revenue > 0:

        df["revenue_share_pct"] = (
            df["total_mrr"]
            / total_revenue
            * 100
        )

    else:

        df["revenue_share_pct"] = 0

    df["cumulative_revenue_share_pct"] = (
        df["revenue_share_pct"]
        .cumsum()
    )

    df["customer_rank"] = (
        np.arange(
            len(df)
        )
        + 1
    )

    return df


# ===================================================================
# PLAN SUMMARY
# ===================================================================

def calculate_plan_summary(
    monthly_snapshot: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate overall plan performance.
    """

    if monthly_snapshot.empty:

        return pd.DataFrame(
            columns=[
                "plan",
                "total_mrr",
                "average_mrr",
                "customers",
                "average_arpu",
            ]
        )

    plan_summary = (
        monthly_snapshot
        .groupby("plan")
        .agg(
            total_mrr=(
                "monthly_revenue",
                "sum",
            ),
            average_mrr=(
                "monthly_revenue",
                "mean",
            ),
            customers=(
                "user_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    plan_summary["average_arpu"] = np.where(
        plan_summary["customers"] > 0,
        (
            plan_summary["total_mrr"]
            / plan_summary["customers"]
        ),
        0,
    )

    return plan_summary.sort_values(
        "total_mrr",
        ascending=False,
    )


# ===================================================================
# SAVE OUTPUTS
# ===================================================================

def save_revenue_outputs(
    revenue_metrics: pd.DataFrame,
    plan_metrics: pd.DataFrame,
    cycle_metrics: pd.DataFrame,
    new_subscriptions: pd.DataFrame,
    cancellations: pd.DataFrame,
    customer_revenue: pd.DataFrame,
    revenue_concentration: pd.DataFrame,
    plan_summary: pd.DataFrame,
) -> None:
    """
    Save all revenue analytics outputs.
    """

    ANALYTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    outputs = {

        "monthly_revenue_metrics.csv":
            revenue_metrics,

        "revenue_by_plan.csv":
            plan_metrics,

        "revenue_by_billing_cycle.csv":
            cycle_metrics,

        "new_subscriptions.csv":
            new_subscriptions,

        "cancellations.csv":
            cancellations,

        "customer_revenue.csv":
            customer_revenue,

        "revenue_concentration.csv":
            revenue_concentration,

        "plan_summary.csv":
            plan_summary,
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


# ===================================================================
# MAIN EXECUTION
# ===================================================================

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS REVENUE ANALYTICS")
    print("=" * 75)

    # ---------------------------------------------------------------
    # LOAD
    # ---------------------------------------------------------------

    print(
        "\nLoading subscriptions..."
    )

    subscriptions = (
        load_subscriptions()
    )

    print(
        f"Subscriptions loaded: "
        f"{len(subscriptions):,}"
    )

    # ---------------------------------------------------------------
    # STANDARDIZE
    # ---------------------------------------------------------------

    print(
        "\nStandardizing subscription columns..."
    )

    subscriptions = (
        standardize_subscription_columns(
            subscriptions
        )
    )

    print(
        "\nStandardized columns:"
    )

    print(
        subscriptions.columns.tolist()
    )

    # ---------------------------------------------------------------
    # MONTHLY REVENUE
    # ---------------------------------------------------------------

    print(
        "\nPreparing monthly recurring revenue..."
    )

    # MRR is already provided by the dataset.
    subscriptions["monthly_revenue"] = (
        subscriptions["price"]
    )

    # ---------------------------------------------------------------
    # MONTHLY SNAPSHOT
    # ---------------------------------------------------------------

    print(
        "Creating monthly subscription snapshot..."
    )

    monthly_snapshot = (
        create_monthly_subscription_snapshot(
            subscriptions
        )
    )

    print(
        f"Snapshot records: "
        f"{len(monthly_snapshot):,}"
    )

    # ---------------------------------------------------------------
    # MRR
    # ---------------------------------------------------------------

    print(
        "Calculating MRR..."
    )

    mrr = calculate_mrr(
        monthly_snapshot
    )

    # ---------------------------------------------------------------
    # ARR
    # ---------------------------------------------------------------

    print(
        "Calculating ARR..."
    )

    revenue_metrics = calculate_arr(
        mrr
    )

    # ---------------------------------------------------------------
    # ARPU
    # ---------------------------------------------------------------

    print(
        "Calculating ARPU..."
    )

    revenue_metrics = calculate_arpu(
        revenue_metrics
    )

    # ---------------------------------------------------------------
    # GROWTH
    # ---------------------------------------------------------------

    print(
        "Calculating revenue growth..."
    )

    revenue_metrics = (
        calculate_revenue_growth(
            revenue_metrics
        )
    )

    # ---------------------------------------------------------------
    # PLAN
    # ---------------------------------------------------------------

    print(
        "Calculating revenue by plan..."
    )

    plan_metrics = (
        calculate_revenue_by_plan(
            monthly_snapshot
        )
    )

    # ---------------------------------------------------------------
    # BILLING
    # ---------------------------------------------------------------

    print(
        "Calculating revenue by billing frequency..."
    )

    cycle_metrics = (
        calculate_revenue_by_billing_cycle(
            monthly_snapshot
        )
    )

    # ---------------------------------------------------------------
    # NEW SUBSCRIPTIONS
    # ---------------------------------------------------------------

    print(
        "Calculating new subscriptions..."
    )

    new_subscriptions = (
        calculate_new_subscriptions(
            subscriptions
        )
    )

    # ---------------------------------------------------------------
    # CANCELLATIONS
    # ---------------------------------------------------------------

    print(
        "Calculating cancellations..."
    )

    cancellations = (
        calculate_cancellations(
            subscriptions
        )
    )

    # ---------------------------------------------------------------
    # CUSTOMER REVENUE
    # ---------------------------------------------------------------

    print(
        "Calculating customer revenue..."
    )

    customer_revenue = (
        calculate_customer_revenue(
            monthly_snapshot
        )
    )

    # ---------------------------------------------------------------
    # REVENUE CONCENTRATION
    # ---------------------------------------------------------------

    print(
        "Calculating revenue concentration..."
    )

    revenue_concentration = (
        calculate_revenue_concentration(
            customer_revenue
        )
    )

    # ---------------------------------------------------------------
    # PLAN SUMMARY
    # ---------------------------------------------------------------

    print(
        "Calculating overall plan performance..."
    )

    plan_summary = (
        calculate_plan_summary(
            monthly_snapshot
        )
    )

    # ---------------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------------

    print(
        "\nSaving revenue analytics..."
    )

    save_revenue_outputs(
        revenue_metrics,
        plan_metrics,
        cycle_metrics,
        new_subscriptions,
        cancellations,
        customer_revenue,
        revenue_concentration,
        plan_summary,
    )

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------

    print(
        "\nRevenue Summary"
    )

    print(
        "-" * 75
    )

    if not revenue_metrics.empty:

        latest = (
            revenue_metrics
            .iloc[-1]
        )

        print(
            f"Latest month: "
            f"{latest['month'].strftime('%Y-%m')}"
        )

        print(
            f"Latest MRR: "
            f"${latest['mrr']:,.2f}"
        )

        print(
            f"Latest ARR: "
            f"${latest['arr']:,.2f}"
        )

        print(
            f"Latest ARPU: "
            f"${latest['arpu']:,.2f}"
        )

        if pd.notna(
            latest["mrr_growth_pct"]
        ):

            print(
                f"Latest MoM MRR Growth: "
                f"{latest['mrr_growth_pct']:.2f}%"
            )

    print(
        f"\nCustomers in revenue data: "
        f"{customer_revenue['user_id'].nunique():,}"
    )

    # ---------------------------------------------------------------
    # TOP PLANS
    # ---------------------------------------------------------------

    print(
        "\nPlan Performance"
    )

    if not plan_summary.empty:

        print(
            plan_summary[
                [
                    "plan",
                    "total_mrr",
                    "customers",
                    "average_arpu",
                ]
            ]
            .to_string(
                index=False
            )
        )

    # ---------------------------------------------------------------
    # TOP CUSTOMERS
    # ---------------------------------------------------------------

    print(
        "\nTop 10 Revenue Customers"
    )

    if not customer_revenue.empty:

        print(
            customer_revenue[
                [
                    "user_id",
                    "total_mrr",
                    "average_monthly_revenue",
                    "active_months",
                ]
            ]
            .head(10)
            .to_string(
                index=False
            )
        )

    # ---------------------------------------------------------------
    # COMPLETE
    # ---------------------------------------------------------------

    print(
        "\n" + "=" * 75
    )

    print(
        "REVENUE ANALYTICS COMPLETE"
    )

    print(
        "=" * 75
    )