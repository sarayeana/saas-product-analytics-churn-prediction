from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = (
    PROJECT_ROOT
    / "data"
)

RAW_DATA_DIR = (
    DATA_DIR
    / "raw"
)

PROCESSED_DATA_DIR = (
    DATA_DIR
    / "processed"
)

ANALYTICS_DATA_DIR = (
    DATA_DIR
    / "analytics"
)


# ============================================================
# MODEL DIRECTORY
# ============================================================

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
)


# ============================================================
# NOTEBOOK DIRECTORY
# ============================================================

NOTEBOOK_DIR = (
    PROJECT_ROOT
    / "Notebooks"
)


# ============================================================
# APPLICATION DIRECTORY
# ============================================================

APP_DIR = (
    PROJECT_ROOT
    / "app"
)


# ============================================================
# IMPORTANT ANALYTICS FILES
# ============================================================

MONTHLY_REVENUE_FILE = (
    ANALYTICS_DATA_DIR
    / "monthly_revenue_metrics.csv"
)

REVENUE_BY_PLAN_FILE = (
    ANALYTICS_DATA_DIR
    / "revenue_by_plan.csv"
)

REVENUE_BY_BILLING_FILE = (
    ANALYTICS_DATA_DIR
    / "revenue_by_billing_cycle.csv"
)

NEW_SUBSCRIPTIONS_FILE = (
    ANALYTICS_DATA_DIR
    / "new_subscriptions.csv"
)

CANCELLATIONS_FILE = (
    ANALYTICS_DATA_DIR
    / "cancellations.csv"
)

CUSTOMER_REVENUE_FILE = (
    ANALYTICS_DATA_DIR
    / "customer_revenue.csv"
)

REVENUE_CONCENTRATION_FILE = (
    ANALYTICS_DATA_DIR
    / "revenue_concentration.csv"
)

PLAN_SUMMARY_FILE = (
    ANALYTICS_DATA_DIR
    / "plan_summary.csv"
)


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

DAILY_PRODUCT_METRICS_FILE = (
    ANALYTICS_DATA_DIR
    / "daily_product_metrics.csv"
)

FEATURE_ADOPTION_FILE = (
    ANALYTICS_DATA_DIR
    / "feature_adoption.csv"
)

PRODUCT_USAGE_FILE = (
    ANALYTICS_DATA_DIR
    / "product_usage_metrics.csv"
)


# ============================================================
# RETENTION
# ============================================================

RETENTION_FILE = (
    ANALYTICS_DATA_DIR
    / "retention_metrics.csv"
)

COHORT_RETENTION_FILE = (
    ANALYTICS_DATA_DIR
    / "cohort_retention.csv"
)


# ============================================================
# CHURN
# ============================================================

CHURN_RISK_FILE = (
    ANALYTICS_DATA_DIR
    / "churn_risk_scores.csv"
)

CHURN_SUMMARY_FILE = (
    ANALYTICS_DATA_DIR
    / "churn_summary.csv"
)

CHURN_FEATURES_FILE = (
    ANALYTICS_DATA_DIR
    / "churn_features.csv"
)

HIGH_RISK_EXPLANATIONS_FILE = (
    ANALYTICS_DATA_DIR
    / "high_risk_customer_explanations.csv"
)

CHURN_PRIORITY_FILE = (
    ANALYTICS_DATA_DIR
    / "churn_priority_customers.csv"
)


# ============================================================
# MODEL EXPLAINABILITY
# ============================================================

MODEL_GLOBAL_IMPORTANCE_FILE = (
    ANALYTICS_DATA_DIR
    / "model_global_importance.csv"
)

MODEL_SHAP_IMPORTANCE_FILE = (
    ANALYTICS_DATA_DIR
    / "model_shap_importance.csv"
)


# ============================================================
# MODEL FILE
# ============================================================

CHURN_MODEL_FILE = (
    MODEL_DIR
    / "churn_prediction_model.pkl"
)


# ============================================================
# DASHBOARD SETTINGS
# ============================================================

APP_TITLE = (
    "SaaS Product Analytics & Churn Prediction"
)

APP_ICON = "📊"

LAYOUT = "wide"


# ============================================================
# RISK SEGMENTS
# ============================================================

RISK_SEGMENTS = [
    "Very Low",
    "Low",
    "Medium",
    "High",
    "Very High",
]


# ============================================================
# PLAN ORDER
# ============================================================

PLAN_ORDER = [
    "Free",
    "Starter",
    "Professional",
    "Enterprise",
]


# ============================================================
# DISPLAY SETTINGS
# ============================================================

TOP_N_CUSTOMERS = 10

TOP_N_FEATURES = 15

TOP_N_RISK_CUSTOMERS = 20


# ============================================================
# VALIDATE IMPORTANT DIRECTORIES
# ============================================================

def validate_project_structure():
    """
    Check whether the major project directories exist.
    """

    required_directories = [
        DATA_DIR,
        PROCESSED_DATA_DIR,
        ANALYTICS_DATA_DIR,
        MODEL_DIR,
        APP_DIR,
    ]

    missing_directories = [
        directory
        for directory in required_directories
        if not directory.exists()
    ]

    if missing_directories:

        print(
            "Warning: Missing directories:"
        )

        for directory in missing_directories:

            print(
                f" - {directory}"
            )

        return False

    return True


if __name__ == "__main__":

    print("=" * 70)
    print(
        "SAAS PROJECT CONFIGURATION"
    )
    print("=" * 70)

    print(
        f"\nProject root:\n{PROJECT_ROOT}"
    )

    print(
        f"\nAnalytics directory:\n"
        f"{ANALYTICS_DATA_DIR}"
    )

    print(
        f"\nModel directory:\n"
        f"{MODEL_DIR}"
    )

    print(
        "\nProject structure valid:",
        validate_project_structure(),
    )