"""
SaaS Churn Prediction
=====================

Purpose
-------
Generate customer-level churn predictions using the best
trained machine-learning model.

Input
-----
data/analytics/churn_features.csv

Model
-----
models/random_forest.pkl
or
models/logistic_regression.pkl

Output
------
data/analytics/churn_predictions.csv

Prediction fields
-----------------
user_id
churn_probability
churn_prediction
risk_segment
risk_score
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# =====================================================================
# PROJECT PATHS
# =====================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ANALYTICS_DIR = (
    PROJECT_ROOT / "data" / "analytics"
)

MODELS_DIR = (
    PROJECT_ROOT / "models"
)


# =====================================================================
# LOAD FEATURES
# =====================================================================

def load_features():
    """
    Load customer-level churn features.
    """

    path = (
        ANALYTICS_DIR
        / "churn_features.csv"
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Churn feature dataset not found:\n"
            f"{path}\n\n"
            f"Run churn_features.py first."
        )

    df = pd.read_csv(path)

    print(
        f"Customer records loaded: "
        f"{len(df):,}"
    )

    return df


# =====================================================================
# LOAD MODEL
# =====================================================================

def load_model(model_name="Random Forest"):
    """
    Load the trained model.

    Default:
        Random Forest
    """

    filename = (
        model_name
        .lower()
        .replace(" ", "_")
        + ".pkl"
    )

    path = (
        MODELS_DIR
        / filename
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Model not found:\n"
            f"{path}\n\n"
            f"Run model_training.py first."
        )

    model = joblib.load(
        path
    )

    print(
        f"Model loaded: "
        f"{model_name}"
    )

    return model


# =====================================================================
# PREPARE FEATURES
# =====================================================================

def prepare_features(df):
    """
    Prepare the exact feature structure expected by the model.
    """

    X = df.drop(
        columns=[
            "churn",
            "user_id",
        ],
        errors="ignore",
    )

    return X


# =====================================================================
# GENERATE PROBABILITIES
# =====================================================================

def generate_predictions(
    model,
    X,
):
    """
    Generate churn probabilities and binary predictions.
    """

    probabilities = (
        model.predict_proba(
            X
        )[:, 1]
    )

    predictions = (
        probabilities >= 0.50
    ).astype(int)

    return (
        probabilities,
        predictions,
    )


# =====================================================================
# CREATE RISK SEGMENT
# =====================================================================

def create_risk_segment(
    probability
):
    """
    Convert churn probability into a business-friendly
    risk segment.

    Risk levels:

        0% - 29.99%  -> Low
        30% - 59.99% -> Medium
        60% - 79.99% -> High
        80% - 100%   -> Critical
    """

    if probability < 0.30:

        return "Low"

    elif probability < 0.60:

        return "Medium"

    elif probability < 0.80:

        return "High"

    else:

        return "Critical"


# =====================================================================
# CREATE RISK SCORE
# =====================================================================

def create_risk_score(
    probability
):
    """
    Convert probability into a 0-100 risk score.
    """

    return round(
        probability * 100,
        2,
    )


# =====================================================================
# CREATE BUSINESS PRIORITY
# =====================================================================

def create_priority(
    probability
):
    """
    Create a retention priority.

    Critical:
        >= 80%

    High:
        >= 60%

    Medium:
        >= 30%

    Low:
        < 30%
    """

    if probability >= 0.80:

        return "Immediate"

    elif probability >= 0.60:

        return "High"

    elif probability >= 0.30:

        return "Monitor"

    else:

        return "Low"


# =====================================================================
# BUILD PREDICTION DATASET
# =====================================================================

def build_prediction_dataset(
    df,
    probabilities,
    predictions,
):
    """
    Create the final customer-level prediction dataset.
    """

    predictions_df = pd.DataFrame(
        {
            "user_id":
                df["user_id"],

            "churn_probability":
                probabilities,

            "churn_prediction":
                predictions,
        }
    )

    # ---------------------------------------------------------------
    # Convert probability to percentage
    # ---------------------------------------------------------------

    predictions_df[
        "churn_probability_pct"
    ] = (
        predictions_df[
            "churn_probability"
        ]
        * 100
    ).round(2)

    # ---------------------------------------------------------------
    # Risk segment
    # ---------------------------------------------------------------

    predictions_df[
        "risk_segment"
    ] = (
        predictions_df[
            "churn_probability"
        ]
        .apply(
            create_risk_segment
        )
    )

    # ---------------------------------------------------------------
    # Risk score
    # ---------------------------------------------------------------

    predictions_df[
        "risk_score"
    ] = (
        predictions_df[
            "churn_probability"
        ]
        .apply(
            create_risk_score
        )
    )

    # ---------------------------------------------------------------
    # Retention priority
    # ---------------------------------------------------------------

    predictions_df[
        "retention_priority"
    ] = (
        predictions_df[
            "churn_probability"
        ]
        .apply(
            create_priority
        )
    )

    return predictions_df


# =====================================================================
# ADD BUSINESS INFORMATION
# =====================================================================

def add_business_information(
    predictions,
    features,
):
    """
    Add useful customer information to the prediction output.

    This makes the final dataset useful for business teams.
    """

    business_columns = [
        "user_id",
        "plan",
        "billing_frequency",
        "monthly_recurring_revenue",
        "annual_contract_value",
        "tenure_days",
        "upgrade_count",
        "downgrade_count",
        "acquisition_source",
        "total_mrr",
        "average_monthly_revenue",
        "active_months",
    ]

    available_columns = [
        column
        for column in business_columns
        if column in features.columns
    ]

    business_df = features[
        available_columns
    ].copy()

    result = predictions.merge(
        business_df,
        on="user_id",
        how="left",
    )

    return result


# =====================================================================
# CREATE RETENTION PRIORITY LIST
# =====================================================================

def create_priority_list(
    predictions
):
    """
    Create a sorted list of customers who should receive
    retention attention first.

    Customers are ranked by:

        1. Churn probability
        2. Monthly recurring revenue
    """

    result = predictions.copy()

    if "monthly_recurring_revenue" in result.columns:

        result = result.sort_values(
            [
                "churn_probability",
                "monthly_recurring_revenue",
            ],
            ascending=[
                False,
                False,
            ],
        )

    else:

        result = result.sort_values(
            "churn_probability",
            ascending=False,
        )

    result[
        "retention_rank"
    ] = range(
        1,
        len(result) + 1,
    )

    return result


# =====================================================================
# SAVE PREDICTIONS
# =====================================================================

def save_predictions(
    predictions
):
    """
    Save customer churn predictions.
    """

    ANALYTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        ANALYTICS_DIR
        / "churn_predictions.csv"
    )

    predictions.to_csv(
        path,
        index=False,
    )

    print(
        f"\nSaved predictions:"
        f"\n{path}"
    )

    return path


# =====================================================================
# SAVE HIGH-RISK CUSTOMERS
# =====================================================================

def save_high_risk_customers(
    predictions
):
    """
    Save customers with >= 60% churn probability.
    """

    high_risk = predictions[
        predictions[
            "churn_probability"
        ] >= 0.60
    ].copy()

    path = (
        ANALYTICS_DIR
        / "high_risk_customers.csv"
    )

    high_risk.to_csv(
        path,
        index=False,
    )

    print(
        f"Saved high-risk customers:"
        f"\n{path}"
    )

    return high_risk


# =====================================================================
# SAVE CRITICAL REVENUE CUSTOMERS
# =====================================================================

def save_critical_revenue_customers(
    predictions
):
    """
    Identify customers who are both:

        - High churn risk
        - Revenue generating

    This creates a practical retention target list.
    """

    if "monthly_recurring_revenue" not in predictions.columns:

        print(
            "\nMonthly recurring revenue not available."
        )

        return None

    critical = predictions[
        (
            predictions[
                "churn_probability"
            ] >= 0.60
        )
        &
        (
            predictions[
                "monthly_recurring_revenue"
            ] > 0
        )
    ].copy()

    critical = critical.sort_values(
        [
            "monthly_recurring_revenue",
            "churn_probability",
        ],
        ascending=[
            False,
            False,
        ],
    )

    path = (
        ANALYTICS_DIR
        / "high_value_at_risk_customers.csv"
    )

    critical.to_csv(
        path,
        index=False,
    )

    print(
        f"Saved high-value at-risk customers:"
        f"\n{path}"
    )

    return critical


# =====================================================================
# PRINT SUMMARY
# =====================================================================

def print_prediction_summary(
    predictions
):
    """
    Print business-oriented prediction summary.
    """

    print(
        "\n" + "=" * 75
    )

    print(
        "CHURN PREDICTION SUMMARY"
    )

    print(
        "=" * 75
    )

    total_customers = len(
        predictions
    )

    predicted_churn = (
        predictions[
            "churn_prediction"
        ]
        .sum()
    )

    print(
        f"\nTotal customers: "
        f"{total_customers:,}"
    )

    print(
        f"Predicted churners: "
        f"{predicted_churn:,}"
    )

    print(
        f"Predicted churn rate: "
        f"{predicted_churn / total_customers * 100:.2f}%"
    )

    # ---------------------------------------------------------------
    # Risk distribution
    # ---------------------------------------------------------------

    print(
        "\nRisk distribution:"
    )

    risk_distribution = (
        predictions[
            "risk_segment"
        ]
        .value_counts()
    )

    for risk, count in (
        risk_distribution.items()
    ):

        percentage = (
            count
            / total_customers
            * 100
        )

        print(
            f"  {risk}: "
            f"{count:,} "
            f"({percentage:.2f}%)"
        )

    # ---------------------------------------------------------------
    # Priority distribution
    # ---------------------------------------------------------------

    print(
        "\nRetention priority:"
    )

    priority_distribution = (
        predictions[
            "retention_priority"
        ]
        .value_counts()
    )

    for priority, count in (
        priority_distribution.items()
    ):

        print(
            f"  {priority}: "
            f"{count:,}"
        )

    # ---------------------------------------------------------------
    # Revenue at risk
    # ---------------------------------------------------------------

    if "monthly_recurring_revenue" in predictions.columns:

        at_risk = predictions[
            predictions[
                "churn_probability"
            ] >= 0.60
        ]

        revenue_at_risk = (
            at_risk[
                "monthly_recurring_revenue"
            ]
            .sum()
        )

        print(
            "\nMonthly recurring revenue at risk:"
        )

        print(
            f"  ${revenue_at_risk:,.2f}"
        )

    # ---------------------------------------------------------------
    # Top 10
    # ---------------------------------------------------------------

    print(
        "\nTop 10 highest-risk customers:"
    )

    top_columns = [
        "user_id",
        "churn_probability_pct",
        "risk_segment",
        "retention_priority",
    ]

    if "monthly_recurring_revenue" in predictions.columns:

        top_columns.append(
            "monthly_recurring_revenue"
        )

    available_top_columns = [
        column
        for column in top_columns
        if column in predictions.columns
    ]

    print(
        predictions[
            available_top_columns
        ]
        .head(10)
        .to_string(
            index=False
        )
    )


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS CUSTOMER CHURN PREDICTION")
    print("=" * 75)

    # ---------------------------------------------------------------
    # Load features
    # ---------------------------------------------------------------

    print(
        "\nLoading customer features..."
    )

    features = load_features()

    # ---------------------------------------------------------------
    # Load model
    # ---------------------------------------------------------------

    print(
        "\nLoading trained model..."
    )

    model = load_model(
        "Random Forest"
    )

    # ---------------------------------------------------------------
    # Prepare features
    # ---------------------------------------------------------------

    print(
        "\nPreparing prediction features..."
    )

    X = prepare_features(
        features
    )

    print(
        f"Prediction features: "
        f"{X.shape[1]}"
    )

    # ---------------------------------------------------------------
    # Generate predictions
    # ---------------------------------------------------------------

    print(
        "\nGenerating churn predictions..."
    )

    (
        probabilities,
        predictions_binary,
    ) = generate_predictions(
        model,
        X,
    )

    # ---------------------------------------------------------------
    # Build prediction dataset
    # ---------------------------------------------------------------

    predictions = (
        build_prediction_dataset(
            features,
            probabilities,
            predictions_binary,
        )
    )

    # ---------------------------------------------------------------
    # Add business information
    # ---------------------------------------------------------------

    print(
        "\nAdding customer business information..."
    )

    predictions = (
        add_business_information(
            predictions,
            features,
        )
    )

    # ---------------------------------------------------------------
    # Priority ranking
    # ---------------------------------------------------------------

    print(
        "Creating retention priority ranking..."
    )

    predictions = (
        create_priority_list(
            predictions
        )
    )

    # ---------------------------------------------------------------
    # Save main predictions
    # ---------------------------------------------------------------

    save_predictions(
        predictions
    )

    # ---------------------------------------------------------------
    # Save high-risk customers
    # ---------------------------------------------------------------

    high_risk = (
        save_high_risk_customers(
            predictions
        )
    )

    # ---------------------------------------------------------------
    # Save high-value customers
    # ---------------------------------------------------------------

    high_value = (
        save_critical_revenue_customers(
            predictions
        )
    )

    # ---------------------------------------------------------------
    # Print summary
    # ---------------------------------------------------------------

    print_prediction_summary(
        predictions
    )

    # ---------------------------------------------------------------
    # Final output
    # ---------------------------------------------------------------

    print(
        "\n" + "=" * 75
    )

    print(
        "CHURN PREDICTION COMPLETE"
    )

    print(
        "=" * 75
    )

    print(
        "\nGenerated files:"
    )

    print(
        "  ✓ churn_predictions.csv"
    )

    print(
        "  ✓ high_risk_customers.csv"
    )

    print(
        "  ✓ high_value_at_risk_customers.csv"
    )