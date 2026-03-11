"""Stage 3: Training with MLflow tracking
Trains a RandomForestClassifier and logs params, metrics, and the model artifact.
"""
import sys
import os
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)

# Ensure we can import sibling modules when run from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from preprocessing import load_and_preprocess

EXPERIMENT_NAME = "income-prediction"

DEFAULT_PARAMS = {
    "n_estimators": 100,
    "max_depth": 5,
    "min_samples_split": 4,
    "class_weight": "balanced",  # handles class imbalance
    "random_state": 42,
}


def compute_metrics(y_true, y_pred, y_prob):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
    }


def train(csv_path: str, params: dict = None, run_name: str = None):
    params = params or DEFAULT_PARAMS

    print(f"\n{'='*50}")
    print("STAGE 3: TRAINING WITH MLFLOW")
    print(f"{'='*50}")

    X_train, X_test, y_train, y_test, feature_names, artifacts = \
        load_and_preprocess(csv_path)

    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=run_name or "rf-baseline") as run:
        run_id = run.info.run_id
        print(f"\nMLflow run ID: {run_id}")

        # Log dataset info
        mlflow.log_param("csv_path", csv_path)
        mlflow.log_param("train_rows", len(X_train))
        mlflow.log_param("test_rows", len(X_test))
        mlflow.log_param("n_features", len(feature_names))

        # Log model params
        mlflow.log_params(params)

        # Train
        clf = RandomForestClassifier(**params)
        clf.fit(X_train, y_train)

        # Evaluate on test set
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
        metrics = compute_metrics(y_test, y_pred, y_prob)

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log feature importances as a tag (compact)
        importances = dict(zip(
            feature_names,
            [round(float(v), 4) for v in clf.feature_importances_]
        ))
        mlflow.set_tag("feature_importances", str(importances))

        # Log model artifact
        mlflow.sklearn.log_model(clf, "random_forest_model")

        print("\nTest metrics:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

        print("\nTop-3 features by importance:")
        top3 = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3]
        for feat, imp in top3:
            print(f"  {feat}: {imp:.4f}")

        return run_id, metrics, clf, artifacts


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/data/sample.csv"
    train(csv_path=path)
