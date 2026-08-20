"""
SaaS Churn Prediction - Model Training
=======================================

Purpose
-------
Train machine-learning models to predict customer churn.

Models
------
1. Logistic Regression
2. Random Forest

Input
-----
data/analytics/churn_features.csv

Output
------
models/
    logistic_regression.pkl
    random_forest.pkl

data/analytics/
    model_comparison.csv

Important
---------
The churn target is:

    churn = 1 -> customer churned
    churn = 0 -> customer retained
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)


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
# LOAD DATA
# =====================================================================

def load_churn_features():
    """
    Load customer-level churn feature dataset.
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
        f"Dataset loaded: "
        f"{len(df):,} rows × "
        f"{len(df.columns):,} columns"
    )

    return df


# =====================================================================
# PREPARE DATA
# =====================================================================

def prepare_data(df):
    """
    Separate features and target.

    user_id is removed because it is an identifier,
    not a meaningful predictive feature.
    """

    df = df.copy()

    if "churn" not in df.columns:

        raise ValueError(
            "Target column 'churn' was not found."
        )

    # ---------------------------------------------------------------
    # Remove identifiers
    # ---------------------------------------------------------------

    X = df.drop(
        columns=[
            "churn",
            "user_id",
        ],
        errors="ignore",
    )

    y = df["churn"].astype(int)

    return X, y


# =====================================================================
# DETECT FEATURE TYPES
# =====================================================================

def detect_feature_types(X):
    """
    Detect numerical and categorical columns.
    """

    numerical_columns = (
        X.select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        X.select_dtypes(
            include=[
                "object",
                "category",
                "bool",
            ]
        )
        .columns
        .tolist()
    )

    return (
        numerical_columns,
        categorical_columns,
    )


# =====================================================================
# CREATE PREPROCESSOR
# =====================================================================

def create_preprocessor(
    numerical_columns,
    categorical_columns,
):
    """
    Create preprocessing pipeline.

    Numerical:
        median imputation
        standard scaling

    Categorical:
        most-frequent imputation
        one-hot encoding
    """

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                numerical_columns,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns,
            ),
        ],
        remainder="drop",
    )

    return preprocessor


# =====================================================================
# CREATE MODELS
# =====================================================================

def create_models():
    """
    Create baseline ML models.
    """

    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42,
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=300,
                max_depth=None,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            ),
    }

    return models


# =====================================================================
# EVALUATE MODEL
# =====================================================================

def evaluate_model(
    model,
    X_test,
    y_test,
):
    """
    Calculate classification metrics.
    """

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    metrics = {

        "accuracy":
            accuracy_score(
                y_test,
                predictions,
            ),

        "precision":
            precision_score(
                y_test,
                predictions,
                zero_division=0,
            ),

        "recall":
            recall_score(
                y_test,
                predictions,
                zero_division=0,
            ),

        "f1":
            f1_score(
                y_test,
                predictions,
                zero_division=0,
            ),

        "roc_auc":
            roc_auc_score(
                y_test,
                probabilities,
            ),
    }

    return metrics


# =====================================================================
# TRAIN MODELS
# =====================================================================

def train_models(
    X_train,
    X_test,
    y_train,
    y_test,
    preprocessor,
    models,
):
    """
    Train and evaluate all models.
    """

    trained_models = []

    for model_name, classifier in models.items():

        print(
            f"\n{'=' * 70}"
        )

        print(
            f"Training: {model_name}"
        )

        print(
            f"{'=' * 70}"
        )

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor,
                ),
                (
                    "classifier",
                    classifier,
                ),
            ]
        )

        # -----------------------------------------------------------
        # Train
        # -----------------------------------------------------------

        pipeline.fit(
            X_train,
            y_train,
        )

        # -----------------------------------------------------------
        # Evaluate
        # -----------------------------------------------------------

        metrics = evaluate_model(
            pipeline,
            X_test,
            y_test,
        )

        print(
            f"Accuracy : "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"Precision: "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"Recall   : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"F1 Score : "
            f"{metrics['f1']:.4f}"
        )

        print(
            f"ROC-AUC  : "
            f"{metrics['roc_auc']:.4f}"
        )

        trained_models.append(
            {
                "model_name": model_name,
                "model": pipeline,
                **metrics,
            }
        )

    return trained_models


# =====================================================================
# SELECT BEST MODEL
# =====================================================================

def select_best_model(
    trained_models,
):
    """
    Select the best model using ROC-AUC.

    ROC-AUC is used because churn prediction is a
    classification problem where probability ranking
    is important.
    """

    best = max(
        trained_models,
        key=lambda x: x["roc_auc"],
    )

    return best


# =====================================================================
# SAVE MODELS
# =====================================================================

def save_models(
    trained_models,
):
    """
    Save trained models to the models directory.
    """

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for result in trained_models:

        model_name = result[
            "model_name"
        ]

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

        joblib.dump(
            result["model"],
            path,
        )

        print(
            f"Saved model: {path}"
        )


# =====================================================================
# SAVE COMPARISON
# =====================================================================

def save_model_comparison(
    trained_models,
):
    """
    Save model comparison table.
    """

    rows = []

    for result in trained_models:

        rows.append(
            {
                "model": result[
                    "model_name"
                ],
                "accuracy": result[
                    "accuracy"
                ],
                "precision": result[
                    "precision"
                ],
                "recall": result[
                    "recall"
                ],
                "f1": result[
                    "f1"
                ],
                "roc_auc": result[
                    "roc_auc"
                ],
            }
        )

    comparison = pd.DataFrame(
        rows
    )

    comparison = comparison.sort_values(
        "roc_auc",
        ascending=False,
    )

    path = (
        ANALYTICS_DIR
        / "model_comparison.csv"
    )

    comparison.to_csv(
        path,
        index=False,
    )

    print(
        f"\nSaved comparison: {path}"
    )

    return comparison


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS CHURN PREDICTION - MODEL TRAINING")
    print("=" * 75)

    # ---------------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------------

    print(
        "\nLoading churn feature dataset..."
    )

    df = load_churn_features()

    # ---------------------------------------------------------------
    # Dataset overview
    # ---------------------------------------------------------------

    print(
        "\nDataset shape:"
    )

    print(
        df.shape
    )

    print(
        "\nTarget distribution:"
    )

    print(
        df["churn"]
        .value_counts()
    )

    print(
        "\nTarget percentage:"
    )

    print(
        (
            df["churn"]
            .value_counts(
                normalize=True
            )
            * 100
        )
    )

    # ---------------------------------------------------------------
    # Prepare data
    # ---------------------------------------------------------------

    print(
        "\nPreparing features..."
    )

    X, y = prepare_data(
        df
    )

    print(
        f"Features: "
        f"{X.shape[1]}"
    )

    print(
        f"Samples: "
        f"{X.shape[0]:,}"
    )

    # ---------------------------------------------------------------
    # Detect feature types
    # ---------------------------------------------------------------

    numerical_columns, categorical_columns = (
        detect_feature_types(X)
    )

    print(
        f"\nNumerical features: "
        f"{len(numerical_columns)}"
    )

    print(
        f"Categorical features: "
        f"{len(categorical_columns)}"
    )

    # ---------------------------------------------------------------
    # Train / test split
    # ---------------------------------------------------------------

    print(
        "\nCreating train/test split..."
    )

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y,
        )
    )

    print(
        f"Training rows: "
        f"{len(X_train):,}"
    )

    print(
        f"Testing rows: "
        f"{len(X_test):,}"
    )

    # ---------------------------------------------------------------
    # Preprocessor
    # ---------------------------------------------------------------

    preprocessor = create_preprocessor(
        numerical_columns,
        categorical_columns,
    )

    # ---------------------------------------------------------------
    # Models
    # ---------------------------------------------------------------

    models = create_models()

    # ---------------------------------------------------------------
    # Train
    # ---------------------------------------------------------------

    trained_models = train_models(
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        models,
    )

    # ---------------------------------------------------------------
    # Save models
    # ---------------------------------------------------------------

    print(
        "\nSaving trained models..."
    )

    save_models(
        trained_models
    )

    # ---------------------------------------------------------------
    # Comparison
    # ---------------------------------------------------------------

    comparison = (
        save_model_comparison(
            trained_models
        )
    )

    # ---------------------------------------------------------------
    # Best model
    # ---------------------------------------------------------------

    best = select_best_model(
        trained_models
    )

    print(
        "\n" + "=" * 75
    )

    print(
        "BEST MODEL"
    )

    print(
        "=" * 75
    )

    print(
        f"Model: "
        f"{best['model_name']}"
    )

    print(
        f"ROC-AUC: "
        f"{best['roc_auc']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best['f1']:.4f}"
    )

    print(
        f"Precision: "
        f"{best['precision']:.4f}"
    )

    print(
        f"Recall: "
        f"{best['recall']:.4f}"
    )

    print(
        "\nModel comparison:"
    )

    print(
        comparison.to_string(
            index=False
        )
    )

    print(
        "\n" + "=" * 75
    )

    print(
        "MODEL TRAINING COMPLETE"
    )

    print(
        "=" * 75
    )