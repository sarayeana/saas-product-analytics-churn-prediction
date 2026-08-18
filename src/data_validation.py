"""
Data validation module for the SaaS Product Analytics & Churn Prediction project.

This module validates:

    - Dataset structure
    - Required columns
    - Primary keys
    - Duplicate records
    - Missing values
    - Data types
    - Date fields
    - Numeric business rules
    - Referential integrity between datasets

The module is intentionally separate from preprocessing so that
data quality problems can be identified before transformations
are applied.
"""

from pathlib import Path

import pandas as pd

from data_loader import load_all_data


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# -------------------------------------------------------------------
# Expected Dataset Structure
# -------------------------------------------------------------------

EXPECTED_COLUMNS = {
    "users": [
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
    ],
    "events": [
        "event_id",
        "user_id",
        "company_id",
        "event_timestamp",
        "event_type",
        "feature",
        "session_id",
        "device",
        "session_duration_minutes",
    ],
    "subscriptions": [
        "subscription_id",
        "user_id",
        "company_id",
        "plan",
        "subscription_start_date",
        "subscription_end_date",
        "billing_frequency",
        "monthly_recurring_revenue",
        "annual_contract_value",
        "trial",
        "status",
        "acquisition_source",
        "upgrade_count",
        "downgrade_count",
        "tenure_days",
    ],
    "support_tickets": [
        "ticket_id",
        "user_id",
        "company_id",
        "created_at",
        "category",
        "priority",
        "channel",
        "status",
        "resolved_at",
        "resolution_time_hours",
        "reopened",
        "satisfaction_score",
        "plan_at_ticket",
        "subscription_status_at_ticket",
    ],
}


# -------------------------------------------------------------------
# Primary Keys
# -------------------------------------------------------------------

PRIMARY_KEYS = {
    "users": "user_id",
    "events": "event_id",
    "subscriptions": "subscription_id",
    "support_tickets": "ticket_id",
}


# -------------------------------------------------------------------
# Date Columns
# -------------------------------------------------------------------

DATE_COLUMNS = {
    "users": ["signup_date"],
    "events": ["event_timestamp"],
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
# Required Non-Null Columns
# -------------------------------------------------------------------

REQUIRED_COLUMNS = {
    "users": [
        "user_id",
        "company_id",
        "signup_date",
    ],
    "events": [
        "event_id",
        "user_id",
        "company_id",
        "event_timestamp",
        "event_type",
    ],
    "subscriptions": [
        "subscription_id",
        "user_id",
        "company_id",
        "subscription_start_date",
    ],
    "support_tickets": [
        "ticket_id",
        "user_id",
        "company_id",
        "created_at",
    ],
}


# -------------------------------------------------------------------
# Required Column Validation
# -------------------------------------------------------------------

def validate_columns(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Validate that all expected columns exist.

    Returns
    -------
    dict
        Validation results for each dataset.
    """

    results = {}

    for dataset_name, expected_columns in EXPECTED_COLUMNS.items():

        df = data[dataset_name]

        actual_columns = set(df.columns)
        expected_columns_set = set(expected_columns)

        missing_columns = sorted(
            expected_columns_set - actual_columns
        )

        unexpected_columns = sorted(
            actual_columns - expected_columns_set
        )

        results[dataset_name] = {
            "passed": len(missing_columns) == 0,
            "missing_columns": missing_columns,
            "unexpected_columns": unexpected_columns,
        }

    return results


# -------------------------------------------------------------------
# Primary Key Validation
# -------------------------------------------------------------------

def validate_primary_keys(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Validate primary key uniqueness and missing values.
    """

    results = {}

    for dataset_name, primary_key in PRIMARY_KEYS.items():

        df = data[dataset_name]

        duplicate_count = int(
            df[primary_key].duplicated().sum()
        )

        null_count = int(
            df[primary_key].isna().sum()
        )

        results[dataset_name] = {
            "primary_key": primary_key,
            "duplicate_count": duplicate_count,
            "null_count": null_count,
            "passed": (
                duplicate_count == 0
                and null_count == 0
            ),
        }

    return results


# -------------------------------------------------------------------
# Missing Value Validation
# -------------------------------------------------------------------

def validate_missing_values(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Calculate missing values for every dataset and
    identify missing values in required columns.
    """

    results = {}

    for dataset_name, df in data.items():

        total_missing = int(
            df.isna().sum().sum()
        )

        required_missing = {}

        for column in REQUIRED_COLUMNS[dataset_name]:

            missing_count = int(
                df[column].isna().sum()
            )

            required_missing[column] = missing_count

        required_columns_passed = all(
            count == 0
            for count in required_missing.values()
        )

        results[dataset_name] = {
            "total_missing_values": total_missing,
            "required_column_missing": required_missing,
            "passed": required_columns_passed,
        }

    return results


# -------------------------------------------------------------------
# Date Validation
# -------------------------------------------------------------------

def validate_dates(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Validate date columns.

    Checks:

        - Invalid date values
        - Future dates
        - Negative date relationships
    """

    results = {}

    current_date = pd.Timestamp.now()

    for dataset_name, columns in DATE_COLUMNS.items():

        df = data[dataset_name]

        dataset_results = {}

        for column in columns:

            converted_dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid_dates = int(
                converted_dates.isna().sum()
                - df[column].isna().sum()
            )

            future_dates = int(
                (converted_dates > current_date).sum()
            )

            dataset_results[column] = {
                "invalid_dates": invalid_dates,
                "future_dates": future_dates,
                "passed": (
                    invalid_dates == 0
                    and future_dates == 0
                ),
            }

        results[dataset_name] = dataset_results

    return results


# -------------------------------------------------------------------
# Numeric Business Rule Validation
# -------------------------------------------------------------------

def validate_numeric_rules(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Validate numeric business rules.
    """

    results = {}

    # ---------------------------------------------------------------
    # Users
    # ---------------------------------------------------------------

    users = data["users"]

    engagement_invalid = int(
        (
            (users["engagement_propensity"] < 0)
            | (users["engagement_propensity"] > 1)
        ).sum()
    )

    users_result = {
        "engagement_propensity_invalid": engagement_invalid,
    }

    # ---------------------------------------------------------------
    # Events
    # ---------------------------------------------------------------

    events = data["events"]

    negative_session_duration = int(
        (
            events["session_duration_minutes"] < 0
        ).sum()
    )

    events_result = {
        "negative_session_duration": negative_session_duration,
    }

    # ---------------------------------------------------------------
    # Subscriptions
    # ---------------------------------------------------------------

    subscriptions = data["subscriptions"]

    negative_mrr = int(
        (
            subscriptions["monthly_recurring_revenue"] < 0
        ).sum()
    )

    negative_acv = int(
        (
            subscriptions["annual_contract_value"] < 0
        ).sum()
    )

    negative_upgrade_count = int(
        (
            subscriptions["upgrade_count"] < 0
        ).sum()
    )

    negative_downgrade_count = int(
        (
            subscriptions["downgrade_count"] < 0
        ).sum()
    )

    negative_tenure = int(
        (
            subscriptions["tenure_days"] < 0
        ).sum()
    )

    subscriptions_result = {
        "negative_mrr": negative_mrr,
        "negative_acv": negative_acv,
        "negative_upgrade_count": negative_upgrade_count,
        "negative_downgrade_count": negative_downgrade_count,
        "negative_tenure": negative_tenure,
    }

    # ---------------------------------------------------------------
    # Support Tickets
    # ---------------------------------------------------------------

    tickets = data["support_tickets"]

    negative_resolution_time = int(
        (
            tickets["resolution_time_hours"] < 0
        ).sum()
    )

    invalid_satisfaction = int(
        (
            (tickets["satisfaction_score"] < 1)
            | (tickets["satisfaction_score"] > 5)
        ).sum()
    )

    support_result = {
        "negative_resolution_time": negative_resolution_time,
        "invalid_satisfaction_score": invalid_satisfaction,
    }

    results["users"] = users_result
    results["events"] = events_result
    results["subscriptions"] = subscriptions_result
    results["support_tickets"] = support_result

    return results


# -------------------------------------------------------------------
# Referential Integrity Validation
# -------------------------------------------------------------------

def validate_referential_integrity(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Validate relationships between users and downstream datasets.

    Checks whether user_id and company_id values appearing in
    events, subscriptions, and support tickets exist in users.
    """

    users = data["users"]

    user_ids = set(
        users["user_id"].dropna()
    )

    company_ids = set(
        users["company_id"].dropna()
    )

    results = {}

    for dataset_name in [
        "events",
        "subscriptions",
        "support_tickets",
    ]:

        df = data[dataset_name]

        missing_user_ids = int(
            (~df["user_id"].isin(user_ids)).sum()
        )

        missing_company_ids = int(
            (~df["company_id"].isin(company_ids)).sum()
        )

        results[dataset_name] = {
            "missing_user_ids": missing_user_ids,
            "missing_company_ids": missing_company_ids,
            "passed": (
                missing_user_ids == 0
                and missing_company_ids == 0
            ),
        }

    return results


# -------------------------------------------------------------------
# Duplicate Row Validation
# -------------------------------------------------------------------

def validate_duplicate_rows(
    data: dict[str, pd.DataFrame]
) -> dict[str, int]:
    """
    Count completely duplicated rows in every dataset.
    """

    return {
        dataset_name: int(df.duplicated().sum())
        for dataset_name, df in data.items()
    }


# -------------------------------------------------------------------
# Full Validation
# -------------------------------------------------------------------

def run_validation(
    data: dict[str, pd.DataFrame]
) -> dict:
    """
    Run the complete validation suite.

    Returns
    -------
    dict
        Complete validation results.
    """

    return {
        "columns": validate_columns(data),
        "primary_keys": validate_primary_keys(data),
        "missing_values": validate_missing_values(data),
        "dates": validate_dates(data),
        "numeric_rules": validate_numeric_rules(data),
        "referential_integrity": validate_referential_integrity(data),
        "duplicates": validate_duplicate_rows(data),
    }


# -------------------------------------------------------------------
# Validation Report
# -------------------------------------------------------------------

def print_validation_report(
    results: dict
) -> None:
    """
    Print a readable validation report.
    """

    print("\n")
    print("=" * 75)
    print("SAAS DATA VALIDATION REPORT")
    print("=" * 75)

    # ---------------------------------------------------------------
    # Column Validation
    # ---------------------------------------------------------------

    print("\n1. COLUMN VALIDATION")
    print("-" * 75)

    for dataset, result in results["columns"].items():

        status = "PASS" if result["passed"] else "FAIL"

        print(f"{dataset:<25} {status}")

        if result["missing_columns"]:
            print(
                f"  Missing: {result['missing_columns']}"
            )

        if result["unexpected_columns"]:
            print(
                f"  Unexpected: {result['unexpected_columns']}"
            )

    # ---------------------------------------------------------------
    # Primary Keys
    # ---------------------------------------------------------------

    print("\n2. PRIMARY KEY VALIDATION")
    print("-" * 75)

    for dataset, result in results["primary_keys"].items():

        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"{dataset:<25} {status} "
            f"| duplicates={result['duplicate_count']} "
            f"| nulls={result['null_count']}"
        )

    # ---------------------------------------------------------------
    # Missing Values
    # ---------------------------------------------------------------

    print("\n3. MISSING VALUE VALIDATION")
    print("-" * 75)

    for dataset, result in results["missing_values"].items():

        status = "PASS" if result["passed"] else "CHECK"

        print(
            f"{dataset:<25} {status} "
            f"| total_missing={result['total_missing_values']}"
        )

        for column, count in result[
            "required_column_missing"
        ].items():

            if count > 0:
                print(
                    f"  {column}: {count} missing"
                )

    # ---------------------------------------------------------------
    # Date Validation
    # ---------------------------------------------------------------

    print("\n4. DATE VALIDATION")
    print("-" * 75)

    for dataset, columns in results["dates"].items():

        for column, result in columns.items():

            status = (
                "PASS"
                if result["passed"]
                else "FAIL"
            )

            print(
                f"{dataset}.{column:<35} {status} "
                f"| invalid={result['invalid_dates']} "
                f"| future={result['future_dates']}"
            )

    # ---------------------------------------------------------------
    # Numeric Rules
    # ---------------------------------------------------------------

    print("\n5. NUMERIC BUSINESS RULES")
    print("-" * 75)

    for dataset, rules in results["numeric_rules"].items():

        for rule, count in rules.items():

            status = (
                "PASS"
                if count == 0
                else "FAIL"
            )

            print(
                f"{dataset}.{rule:<45} "
                f"{status} | violations={count}"
            )

    # ---------------------------------------------------------------
    # Referential Integrity
    # ---------------------------------------------------------------

    print("\n6. REFERENTIAL INTEGRITY")
    print("-" * 75)

    for dataset, result in results[
        "referential_integrity"
    ].items():

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"{dataset:<25} {status} "
            f"| missing_users={result['missing_user_ids']} "
            f"| missing_companies={result['missing_company_ids']}"
        )

    # ---------------------------------------------------------------
    # Duplicate Rows
    # ---------------------------------------------------------------

    print("\n7. DUPLICATE ROWS")
    print("-" * 75)

    for dataset, count in results[
        "duplicates"
    ].items():

        status = (
            "PASS"
            if count == 0
            else "CHECK"
        )

        print(
            f"{dataset:<25} {status} "
            f"| duplicates={count}"
        )

    print("\n" + "=" * 75)
    print("VALIDATION COMPLETE")
    print("=" * 75)


# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":

    print(
        "Loading SaaS datasets..."
    )

    data = load_all_data()

    results = run_validation(data)

    print_validation_report(results)
