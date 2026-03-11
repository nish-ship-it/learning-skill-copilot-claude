"""MLOps Pipeline Orchestrator
Runs all 4 stages in sequence: validate → preprocess → train → evaluate.

Usage:
  python examples/src/pipeline_runner.py
  python examples/src/pipeline_runner.py examples/data/sample.csv
  python examples/src/pipeline_runner.py examples/data/sample.csv --n-estimators 200 --max-depth 8

Designed to demonstrate skills: validate-data, train-model, evaluate-model.
"""
import sys
import os
import argparse

# Ensure sibling imports work when run from repo root
sys.path.insert(0, os.path.dirname(__file__))

from data_validation import validate, main as validate_main
from train_mlflow import train, DEFAULT_PARAMS
from evaluate import main as evaluate_main


def parse_args():
    p = argparse.ArgumentParser(description="MLOps Pipeline Runner")
    p.add_argument("csv", nargs="?", default="examples/data/sample.csv")
    p.add_argument("--n-estimators", type=int, default=100)
    p.add_argument("--max-depth", type=int, default=5)
    p.add_argument("--run-name", default=None)
    return p.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 60)
    print("  MLOPS PIPELINE: INCOME PREDICTION")
    print("=" * 60)
    print(f"  Data: {args.csv}")
    print(f"  n_estimators={args.n_estimators}, max_depth={args.max_depth}")

    # Stage 1: Validate
    validation = validate_main(args.csv)
    if not validation["passed"]:
        print("\n✗ Pipeline aborted: data validation failed.")
        sys.exit(1)

    # Stage 2+3: Preprocess + Train (preprocessing is called inside train_mlflow)
    params = {
        **DEFAULT_PARAMS,
        "n_estimators": args.n_estimators,
        "max_depth": args.max_depth,
    }
    run_id, metrics, clf, artifacts = train(
        csv_path=args.csv,
        params=params,
        run_name=args.run_name,
    )

    # Stage 4: Evaluate (show leaderboard)
    evaluate_main()

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE ✓")
    print(f"  MLflow run ID : {run_id}")
    print(f"  Accuracy      : {metrics['accuracy']:.4f}")
    print(f"  F1            : {metrics['f1']:.4f}")
    print(f"  ROC-AUC       : {metrics['roc_auc']:.4f}")
    print("=" * 60)

    return run_id, metrics


if __name__ == "__main__":
    main()
