---
name: evaluate-model
description: >
  Compare MLflow experiment runs and find the best model. Use when the user says:
  "evaluate the model", "compare experiment runs", "which run is best",
  "show MLflow results", "show model performance", "compare models",
  "what's the best F1 score", "show the leaderboard", "Stage 4 evaluation",
  "which hyperparameters worked best".
---

# evaluate-model skill

Compare all MLflow runs and surface the best-performing model.

## Show the leaderboard

```bash
python examples/src/evaluate.py
```

This prints a table of **all runs**, sorted by F1 score, with key metrics and hyperparameters side-by-side.

## Show detail for a single run

```bash
python examples/src/evaluate.py <run_id>
# Example: python examples/src/evaluate.py a3b1c2d4
```

This prints every param, metric, and tag for that run.

## Launch the MLflow UI

```bash
mlflow ui --port 5000
```

Open **http://127.0.0.1:5000** in your browser to:
- See all runs in the `income-prediction` experiment
- Compare metrics side-by-side with charts
- Download model artifacts
- Filter and sort runs interactively

## Metrics explained

| Metric | What it means | Good when... |
|---|---|---|
| `accuracy` | % of correct predictions | Classes are balanced |
| `precision` | Of all predicted >50K, how many are right | False positives are costly |
| `recall` | Of all actual >50K, how many were caught | False negatives are costly |
| `f1` | Harmonic mean of precision and recall | **Best single metric here** (imbalanced data) |
| `roc_auc` | Area under ROC curve | Want threshold-agnostic view |

> **Why F1?** The dataset has class imbalance (63% `<=50K`). Accuracy alone is misleading — a model that always predicts `<=50K` gets 63% accuracy. F1 penalises both precision and recall failures.

## Interpreting results

After showing the leaderboard, tell the user:

1. Which run has the best F1 and ROC-AUC
2. Whether the best params suggest under/overfitting (low depth → underfitting, high depth → overfitting risk)
3. What to try next — e.g., feature engineering, SMOTE for imbalance, gradient boosting

## Load the best model for inference

```python
import mlflow.sklearn
model = mlflow.sklearn.load_model("mlruns/<experiment_id>/<run_id>/artifacts/random_forest_model")
predictions = model.predict(X_new)
```
