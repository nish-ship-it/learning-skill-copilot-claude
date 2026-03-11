---
name: train-model
description: >
  Train a machine learning model with MLflow experiment tracking. Use when the user says:
  "train the model", "run training", "start an experiment", "train with MLflow",
  "run the ML pipeline", "fit the classifier", "train income prediction model",
  "log a new experiment run", "Stage 3 training".
---

# train-model skill

Run the full **MLOps pipeline** (validate → preprocess → train → evaluate) with MLflow tracking.

## Basic usage

```bash
# Run with default hyperparameters
python examples/src/pipeline_runner.py

# Run with custom hyperparameters
python examples/src/pipeline_runner.py examples/data/sample.csv \
  --n-estimators 200 \
  --max-depth 8 \
  --run-name my-experiment
```

## What gets tracked in MLflow

Every training run automatically logs:

| Category | What's logged |
|---|---|
| **Params** | `n_estimators`, `max_depth`, `min_samples_split`, `class_weight`, `random_state`, row counts |
| **Metrics** | `accuracy`, `f1`, `precision`, `recall`, `roc_auc` |
| **Artifacts** | Serialised `RandomForestClassifier` model (loadable with `mlflow.sklearn.load_model`) |
| **Tags** | Feature importances dictionary |

## Run multiple experiments

To compare hyperparameters, run the pipeline multiple times with different settings:

```bash
python examples/src/pipeline_runner.py --n-estimators 50  --max-depth 3 --run-name shallow
python examples/src/pipeline_runner.py --n-estimators 100 --max-depth 5 --run-name baseline
python examples/src/pipeline_runner.py --n-estimators 200 --max-depth 8 --run-name deep
```

Then compare with the **evaluate-model** skill or the MLflow UI:

```bash
mlflow ui --port 5000
# Open http://127.0.0.1:5000 in your browser
```

## MLflow tracking directory

Runs are stored locally in `mlruns/` at the repo root. The experiment is named `income-prediction`.

## Key design decisions

- **`class_weight='balanced'`** — automatically compensates for the 63/37 class imbalance in the dataset.
- **`stratify=y`** in train/test split — preserves class ratio in both splits.
- **Median imputation** — fills the 5–6% missing values in `age` and `hours_per_week`.

## After training

Ask the user if they want to:
1. Compare runs → use the **evaluate-model** skill
2. Launch the MLflow UI to explore runs visually
3. Run with different hyperparameters to see how metrics change
