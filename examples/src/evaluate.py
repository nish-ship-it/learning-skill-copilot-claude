"""Stage 4: Evaluation — compare MLflow runs and surface the best model.
Usage:
  python examples/src/evaluate.py                  # show all runs in experiment
  python examples/src/evaluate.py <run_id>          # show single run details
"""
import sys
import mlflow
import pandas as pd

EXPERIMENT_NAME = "income-prediction"
KEY_METRICS = ["accuracy", "f1", "roc_auc", "precision", "recall"]


def get_all_runs():
    client = mlflow.MlflowClient()
    try:
        exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    except Exception:
        return pd.DataFrame()
    if exp is None:
        return pd.DataFrame()

    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=["metrics.f1 DESC"],
    )
    if not runs:
        return pd.DataFrame()

    records = []
    for r in runs:
        row = {"run_id": r.info.run_id[:8], "run_name": r.info.run_name or ""}
        for m in KEY_METRICS:
            row[m] = round(r.data.metrics.get(m, float("nan")), 4)
        row["n_estimators"] = r.data.params.get("n_estimators", "?")
        row["max_depth"] = r.data.params.get("max_depth", "?")
        records.append(row)
    return pd.DataFrame(records)


def show_run_detail(run_id: str):
    client = mlflow.MlflowClient()
    run = client.get_run(run_id)
    print(f"\nRun: {run_id}")
    print(f"Name: {run.info.run_name}")
    print("\nParams:")
    for k, v in run.data.params.items():
        print(f"  {k}: {v}")
    print("\nMetrics:")
    for k, v in run.data.metrics.items():
        print(f"  {k}: {v:.4f}")
    print("\nTags:")
    for k, v in run.data.tags.items():
        if not k.startswith("mlflow."):
            print(f"  {k}: {v}")


def main(run_id: str = None):
    print(f"\n{'='*50}")
    print("STAGE 4: EVALUATION")
    print(f"{'='*50}")
    print(f"Experiment: {EXPERIMENT_NAME}")

    # Accept run_id from arg or from CLI argv (not from parent's argv)
    if run_id is None and len(sys.argv) > 1 and sys.argv[0].endswith("evaluate.py"):
        run_id = sys.argv[1]

    if run_id:
        show_run_detail(run_id)
        return

    df = get_all_runs()
    if df.empty:
        print("No runs found. Run train_mlflow.py first.")
        return

    print(f"\nAll runs ({len(df)} total), sorted by F1:\n")
    print(df.to_string(index=False))

    best = df.iloc[0]
    print(f"\n✓ Best run: {best['run_id']} | F1={best['f1']:.4f} | ROC-AUC={best['roc_auc']:.4f}")


if __name__ == "__main__":
    main()
