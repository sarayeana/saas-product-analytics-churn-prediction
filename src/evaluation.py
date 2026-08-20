"""
SaaS Churn Prediction - Model Evaluation
=========================================

Purpose
-------
Perform detailed evaluation of trained churn prediction models.

Evaluation includes
-------------------
    - Accuracy
    - Precision
    - Recall
    - F1 Score
    - ROC-AUC
    - Confusion Matrix
    - Classification Report
    - ROC Curve
    - Precision-Recall Curve
    - Feature Importance

Input
-----
data/analytics/churn_features.csv

Models
------
models/logistic_regression.pkl
models/random_forest.pkl

Outputs
-------
data/analytics/model_evaluation.csv

reports/
    confusion_matrix_*.png
    roc_curve_*.png
    precision_recall_*.png
    feature_importance_*.csv
"""


from pathlib import Path

import joblib
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
    average_precision_score,
)
from sklearn.model_selection import train_test_split


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

REPORTS_DIR = (
    PROJECT_ROOT / "reports"
)


# =====================================================================
# LOAD DATA
# =====================================================================

def load_churn_data():
    """
    Load the same churn feature dataset used during model training.
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
        f"{len(df):,} rows"
    )

    return df


# =====================================================================
# PREPARE DATA
# =====================================================================

def prepare_evaluation_data(df):
    """
    Prepare X and y for model evaluation.

    This must match the training setup.
    """

    if "churn" not in df.columns:

        raise ValueError(
            "Target column 'churn' not found."
        )

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
# TRAIN / TEST SPLIT
# =====================================================================

def create_test_set(X, y):
    """
    Recreate the same deterministic test split used during training.

    random_state=42 and stratification ensure that the same
    customers are placed into the test set.
    """

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


# =====================================================================
# LOAD MODEL
# =====================================================================

def load_model(model_name):
    """
    Load a trained model pipeline.
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
        f"Loaded model: "
        f"{model_name}"
    )

    return model


# =====================================================================
# EVALUATE CLASSIFICATION MODEL
# =====================================================================

def evaluate_model(
    model,
    X_test,
    y_test,
):
    """
    Calculate comprehensive classification metrics.
    """

    predictions = (
        model.predict(
            X_test
        )
    )

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

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

        "average_precision":
            average_precision_score(
                y_test,
                probabilities,
            ),
    }

    return (
        metrics,
        predictions,
        probabilities,
    )


# =====================================================================
# CONFUSION MATRIX
# =====================================================================

def save_confusion_matrix(
    model_name,
    y_test,
    predictions,
):
    """
    Save confusion matrix visualization.
    """

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    figure, axis = plt.subplots(
        figsize=(7, 6)
    )

    image = axis.imshow(
        matrix
    )

    axis.set_title(
        f"Confusion Matrix - {model_name}"
    )

    axis.set_xlabel(
        "Predicted Label"
    )

    axis.set_ylabel(
        "Actual Label"
    )

    axis.set_xticks(
        [0, 1]
    )

    axis.set_yticks(
        [0, 1]
    )

    axis.set_xticklabels(
        [
            "Retained",
            "Churned",
        ]
    )

    axis.set_yticklabels(
        [
            "Retained",
            "Churned",
        ]
    )

    # Add values to matrix cells.

    for row in range(2):

        for column in range(2):

            axis.text(
                column,
                row,
                matrix[row, column],
                ha="center",
                va="center",
            )

    figure.tight_layout()

    path = (
        REPORTS_DIR
        / (
            model_name
            .lower()
            .replace(" ", "_")
            + "_confusion_matrix.png"
        )
    )

    figure.savefig(
        path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        f"Saved: {path}"
    )

    return matrix


# =====================================================================
# ROC CURVE
# =====================================================================

def save_roc_curve(
    model_name,
    y_test,
    probabilities,
):
    """
    Save ROC curve.
    """

    false_positive_rate, true_positive_rate, _ = (
        roc_curve(
            y_test,
            probabilities,
        )
    )

    auc_score = (
        roc_auc_score(
            y_test,
            probabilities,
        )
    )

    figure, axis = plt.subplots(
        figsize=(8, 6)
    )

    axis.plot(
        false_positive_rate,
        true_positive_rate,
        label=f"ROC-AUC = {auc_score:.4f}",
    )

    axis.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
    )

    axis.set_title(
        f"ROC Curve - {model_name}"
    )

    axis.set_xlabel(
        "False Positive Rate"
    )

    axis.set_ylabel(
        "True Positive Rate"
    )

    axis.legend()

    figure.tight_layout()

    path = (
        REPORTS_DIR
        / (
            model_name
            .lower()
            .replace(" ", "_")
            + "_roc_curve.png"
        )
    )

    figure.savefig(
        path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        f"Saved: {path}"
    )


# =====================================================================
# PRECISION-RECALL CURVE
# =====================================================================

def save_precision_recall_curve(
    model_name,
    y_test,
    probabilities,
):
    """
    Save precision-recall curve.
    """

    precision, recall, _ = (
        precision_recall_curve(
            y_test,
            probabilities,
        )
    )

    average_precision = (
        average_precision_score(
            y_test,
            probabilities,
        )
    )

    figure, axis = plt.subplots(
        figsize=(8, 6)
    )

    axis.plot(
        recall,
        precision,
        label=(
            f"Average Precision = "
            f"{average_precision:.4f}"
        ),
    )

    axis.set_title(
        f"Precision-Recall Curve - {model_name}"
    )

    axis.set_xlabel(
        "Recall"
    )

    axis.set_ylabel(
        "Precision"
    )

    axis.legend()

    figure.tight_layout()

    path = (
        REPORTS_DIR
        / (
            model_name
            .lower()
            .replace(" ", "_")
            + "_precision_recall_curve.png"
        )
    )

    figure.savefig(
        path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        f"Saved: {path}"
    )


# =====================================================================
# CLASSIFICATION REPORT
# =====================================================================

def save_classification_report(
    model_name,
    y_test,
    predictions,
):
    """
    Save detailed classification report.
    """

    report = classification_report(
        y_test,
        predictions,
        target_names=[
            "Retained",
            "Churned",
        ],
        zero_division=0,
    )

    path = (
        REPORTS_DIR
        / (
            model_name
            .lower()
            .replace(" ", "_")
            + "_classification_report.txt"
        )
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            f"Classification Report - "
            f"{model_name}\n"
        )

        file.write(
            "=" * 60
            + "\n\n"
        )

        file.write(
            report
        )

    print(
        f"Saved: {path}"
    )


# =====================================================================
# FEATURE IMPORTANCE
# =====================================================================

def extract_feature_importance(
    model,
):
    """
    Extract feature importance from a trained pipeline.

    Works with:
        - Logistic Regression
        - Random Forest
    """

    if "preprocessor" not in model.named_steps:

        return None

    if "classifier" not in model.named_steps:

        return None

    preprocessor = model.named_steps[
        "preprocessor"
    ]

    classifier = model.named_steps[
        "classifier"
    ]

    # ---------------------------------------------------------------
    # Get transformed feature names
    # ---------------------------------------------------------------

    try:

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )

    except Exception:

        return None

    # ---------------------------------------------------------------
    # Random Forest
    # ---------------------------------------------------------------

    if hasattr(
        classifier,
        "feature_importances_",
    ):

        importance = (
            classifier
            .feature_importances_
        )

    # ---------------------------------------------------------------
    # Logistic Regression
    # ---------------------------------------------------------------

    elif hasattr(
        classifier,
        "coef_",
    ):

        importance = np.abs(
            classifier
            .coef_[0]
        )

    else:

        return None

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importance,
        }
    )

    importance_df = (
        importance_df
        .sort_values(
            "importance",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )

    return importance_df


# =====================================================================
# SAVE FEATURE IMPORTANCE
# =====================================================================

def save_feature_importance(
    model_name,
    model,
):
    """
    Save feature importance to CSV.
    """

    importance_df = (
        extract_feature_importance(
            model
        )
    )

    if importance_df is None:

        print(
            f"No feature importance available "
            f"for {model_name}"
        )

        return None

    path = (
        ANALYTICS_DIR
        / (
            model_name
            .lower()
            .replace(" ", "_")
            + "_feature_importance.csv"
        )
    )

    importance_df.to_csv(
        path,
        index=False,
    )

    print(
        f"Saved: {path}"
    )

    return importance_df


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":

    print("=" * 75)
    print("SAAS CHURN MODEL EVALUATION")
    print("=" * 75)

    # ---------------------------------------------------------------
    # Create output directories
    # ---------------------------------------------------------------

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    ANALYTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------------
    # Load data
    # ---------------------------------------------------------------

    print(
        "\nLoading churn dataset..."
    )

    df = load_churn_data()

    X, y = prepare_evaluation_data(
        df
    )

    # ---------------------------------------------------------------
    # Recreate test split
    # ---------------------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = create_test_set(
        X,
        y,
    )

    print(
        f"Evaluation rows: "
        f"{len(X_test):,}"
    )

    # ---------------------------------------------------------------
    # Models
    # ---------------------------------------------------------------

    model_names = [
        "Logistic Regression",
        "Random Forest",
    ]

    results = []

    # ---------------------------------------------------------------
    # Evaluate each model
    # ---------------------------------------------------------------

    for model_name in model_names:

        print(
            "\n" + "=" * 75
        )

        print(
            f"EVALUATING: {model_name}"
        )

        print(
            "=" * 75
        )

        model = load_model(
            model_name
        )

        # -----------------------------------------------------------
        # Metrics
        # -----------------------------------------------------------

        (
            metrics,
            predictions,
            probabilities,
        ) = evaluate_model(
            model,
            X_test,
            y_test,
        )

        print(
            "\nPerformance:"
        )

        print(
            f"Accuracy: "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"Precision: "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"Recall: "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"F1: "
            f"{metrics['f1']:.4f}"
        )

        print(
            f"ROC-AUC: "
            f"{metrics['roc_auc']:.4f}"
        )

        print(
            f"Average Precision: "
            f"{metrics['average_precision']:.4f}"
        )

        # -----------------------------------------------------------
        # Confusion matrix
        # -----------------------------------------------------------

        matrix = save_confusion_matrix(
            model_name,
            y_test,
            predictions,
        )

        print(
            "\nConfusion Matrix:"
        )

        print(
            matrix
        )

        # -----------------------------------------------------------
        # ROC curve
        # -----------------------------------------------------------

        save_roc_curve(
            model_name,
            y_test,
            probabilities,
        )

        # -----------------------------------------------------------
        # Precision-recall
        # -----------------------------------------------------------

        save_precision_recall_curve(
            model_name,
            y_test,
            probabilities,
        )

        # -----------------------------------------------------------
        # Classification report
        # -----------------------------------------------------------

        save_classification_report(
            model_name,
            y_test,
            predictions,
        )

        # -----------------------------------------------------------
        # Feature importance
        # -----------------------------------------------------------

        save_feature_importance(
            model_name,
            model,
        )

        # -----------------------------------------------------------
        # Store metrics
        # -----------------------------------------------------------

        results.append(
            {
                "model": model_name,
                **metrics,
            }
        )

    # ---------------------------------------------------------------
    # Save evaluation summary
    # ---------------------------------------------------------------

    evaluation_df = pd.DataFrame(
        results
    )

    evaluation_df = (
        evaluation_df
        .sort_values(
            "roc_auc",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )

    evaluation_path = (
        ANALYTICS_DIR
        / "model_evaluation.csv"
    )

    evaluation_df.to_csv(
        evaluation_path,
        index=False,
    )

    # ---------------------------------------------------------------
    # Final summary
    # ---------------------------------------------------------------

    print(
        "\n" + "=" * 75
    )

    print(
        "MODEL EVALUATION SUMMARY"
    )

    print(
        "=" * 75
    )

    print(
        evaluation_df.to_string(
            index=False
        )
    )

    best_model = (
        evaluation_df
        .iloc[0]
    )

    print(
        "\nBest model:"
    )

    print(
        f"  {best_model['model']}"
    )

    print(
        f"ROC-AUC: "
        f"{best_model['roc_auc']:.4f}"
    )

    print(
        f"F1 Score: "
        f"{best_model['f1']:.4f}"
    )

    print(
        f"Recall: "
        f"{best_model['recall']:.4f}"
    )

    print(
        "\n" + "=" * 75
    )

    print(
        "MODEL EVALUATION COMPLETE"
    )

    print(
        "=" * 75
    )