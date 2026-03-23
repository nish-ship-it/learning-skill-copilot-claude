---
name: tune-hyperparameters
description: >
  Use this skill when the user wants to tune, optimise, or search for the best
  hyperparameters for a model. Trigger phrases include: "tune hyperparameters",
  "find the best params", "grid search", "hyperparameter optimisation", "improve
  accuracy", "which n_estimators should I use", "what max_depth works best",
  "run a parameter sweep".
---

# tune-hyperparameters skill

Run a **hyperparameter sweep** over the MLOps pipeline to find the combination of
`n_estimators` and `max_depth` that produces the highest F1 score.

## Basic usage

```bash
# Run a quick 3-configuration sweep (shallow / baseline / deep)
python examples/src/pipeline_runner.py --n-estimators 50  --max-depth 3 --run-name sweep-shallow
python examples/src/pipeline_runner.py --n-estimators 100 --max-depth 5 --run-name sweep-baseline
python examples/src/pipeline_runner.py --n-estimators 200 --max-depth 8 --run-name sweep-deep
```

After all runs complete, compare results with the **evaluate-model** skill:

```bash
python examples/src/evaluate.py
```

## Suggested parameter grid

| `n_estimators` | `max_depth` | Expected behaviour |
|---|---|---|
| 50 | 3 | Fast, high bias — good baseline |
| 100 | 5 | Balanced — usually the best starting point |
| 200 | 8 | Slower, lower bias — watch for overfitting |
| 300 | None | Fully grown trees — high variance |

## What to look for in the results

- **F1 score** — primary metric for the imbalanced income-prediction dataset.
- **ROC-AUC** — useful secondary metric; should stay above 0.85 for a healthy model.
- **Overfitting signal** — if training accuracy is ≫ test accuracy, reduce `max_depth`.

## View all runs in MLflow UI

```bash
mlflow ui --port 5000
# Open http://127.0.0.1:5000 → select experiment "income-prediction"
# Sort by f1 descending to find the best run
```

## After tuning

Ask the user if they want to:
1. Retrain the winning configuration with a stable `--run-name` (e.g. `best-model`)
2. Export the best model artifact for deployment
3. Return to **evaluate-model** to generate a final leaderboard
