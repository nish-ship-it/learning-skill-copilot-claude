# MLOps with Copilot Skills

This guide shows how the `validate-data`, `train-model`, and `evaluate-model` skills map to a proper MLOps workflow backed by **MLflow**.

---

## The 4-Stage Pipeline

```
CSV Data
  │
  ▼
┌─────────────────────┐
│ Stage 1: Validate   │  ← validate-data skill
│ schema, nulls,      │
│ class balance       │
└────────┬────────────┘
         │ PASSED ✓
         ▼
┌─────────────────────┐
│ Stage 2: Preprocess │  (runs inside train-model skill)
│ impute, encode,     │
│ scale, split        │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ Stage 3: Train      │  ← train-model skill
│ RandomForest +      │
│ MLflow tracking     │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ Stage 4: Evaluate   │  ← evaluate-model skill
│ leaderboard,        │
│ best run, MLflow UI │
└─────────────────────┘
```

---

## Running the Full Pipeline

```bash
# Activate the virtual environment
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

# Run with default hyperparameters
python examples/src/pipeline_runner.py

# Run with custom hyperparameters
python examples/src/pipeline_runner.py examples/data/sample.csv \
  --n-estimators 200 \
  --max-depth 8 \
  --run-name my-experiment

# Compare runs
python examples/src/evaluate.py

# Open interactive UI
mlflow ui --port 5000
```

---

## Dataset: What Changed and Why It Matters

The dataset grew from **25 rows / 6 columns** to **220 rows / 9 columns**. Each change was deliberate — it forces the pipeline to solve a real-world problem.

### Size & balance

| Property | v1 (original) | v2 (current) |
|---|---|---|
| Rows | 25 | **220** |
| Test split size | 5 rows (meaningless) | **44 rows** (statistically valid) |
| Class balance | 52% / 48% (balanced) | **63% / 37%** (mild imbalance) |
| Minority class | — | 82 rows labelled `>50K` |

**Why imbalance matters:** A model that always predicts `<=50K` gets **63% accuracy** without learning anything. That's why we track F1 and ROC-AUC instead, and use `class_weight='balanced'` in training.

### New features

| Column | Type | Why added |
|---|---|---|
| `marital_status` | categorical (5 values) | Correlated with income in real census data |
| `gender` | categorical (2 values) | Common fairness audit dimension |
| `native_country` | categorical (7 values) | Adds cardinality — harder for encoder to generalise |

### Missing values (new in v2)

| Column | Missing count | Missing % | How handled |
|---|---|---|---|
| `age` | 5 | 2.3% | Median imputation in `preprocessing.py` |
| `hours_per_week` | 7 | 3.2% | Median imputation in `preprocessing.py` |

Both are **below the 20% threshold** in `data_validation.py` so the pipeline warns but continues. If either exceeded 20%, Stage 1 would abort.

**Why float dtype for age?** pandas converts integer columns containing `NaN` to `float64` automatically — that's why `age` appears as `float64` in the schema.

### Impact on the pipeline stages

| Stage | v1 behaviour | v2 behaviour |
|---|---|---|
| Validate | Not needed (simple, clean data) | Checks 9 columns, catches nulls, warns on imbalance |
| Preprocess | 1 LabelEncoder (occupation only) | Median imputer + 4 LabelEncoders + StandardScaler |
| Train | No class weighting needed | `class_weight='balanced'` required |
| Evaluate | Accuracy sufficient | F1 + ROC-AUC needed to see past majority-class bias |

---

## Skills in Detail

### `validate-data`

Trigger: *"validate my data"*, *"check data quality"*, *"is my CSV ready?"*

Runs `examples/src/data_validation.py` which checks:
- All required columns present
- No column has > 20% nulls
- Target values are only `>50K` or `<=50K`
- Warns if any column has 1–20% nulls (will be imputed)
- Warns if minority class < 10%

### `train-model`

Trigger: *"train the model"*, *"run the ML pipeline"*, *"start an experiment"*

Runs `examples/src/pipeline_runner.py` which:
1. Calls `data_validation.py` (Stage 1)
2. Calls `preprocessing.py` (Stage 2) — imputation → encoding → scaling → stratified split
3. Trains `RandomForestClassifier` with `class_weight='balanced'`
4. Logs params, metrics, and the model artifact to MLflow
5. Prints the evaluation leaderboard

Each run gets a unique **run ID** and is stored in `mlruns/`.

### `evaluate-model`

Trigger: *"compare runs"*, *"show the leaderboard"*, *"which run is best?"*

Runs `examples/src/evaluate.py` which:
- Fetches all runs from the `income-prediction` experiment
- Sorts by F1 (best metric for imbalanced data)
- Prints side-by-side metrics and hyperparameters
- Identifies the best run

---

## What Gets Logged to MLflow

| Category | Values |
|---|---|
| **Params** | `n_estimators`, `max_depth`, `min_samples_split`, `class_weight`, row counts |
| **Metrics** | `accuracy`, `f1`, `precision`, `recall`, `roc_auc` |
| **Artifacts** | Serialised `RandomForestClassifier` model |
| **Tags** | Feature importances dictionary |

---

## Results from the First Two Runs

| Run | n_estimators | max_depth | F1 | ROC-AUC |
|---|---|---|---|---|
| baseline | 100 | 5 | **0.667** | **0.795** |
| deep | 200 | 8 | 0.593 | 0.786 |

**Insight:** A deeper tree (max_depth=8) overfit — recall dropped from 62.5% to 50%. The shallower baseline generalised better.

---

## Adding More Experiments

Ideas to try (and compare in the leaderboard):

```bash
# Shallow (underfitting check)
python examples/src/pipeline_runner.py --n-estimators 50 --max-depth 3 --run-name shallow

# Wide forest
python examples/src/pipeline_runner.py --n-estimators 300 --max-depth 5 --run-name wide

# Deep forest
python examples/src/pipeline_runner.py --n-estimators 100 --max-depth 10 --run-name very-deep
```

---

## MLflow UI

```bash
mlflow ui --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) to:

- Compare runs with interactive charts
- Filter and sort by any metric
- Download model artifacts
- See feature importance tags

The `mlruns/` directory at the repo root stores all run data locally — no external service needed.

---

## File Map

```
examples/
├── data/
│   └── sample.csv              ← 220-row dataset (9 features)
├── notebooks/
│   └── eda_demo.ipynb          ← EDA with charts (executed)
└── src/
    ├── data_validation.py      ← Stage 1: schema + null + balance checks
    ├── preprocessing.py        ← Stage 2: impute + encode + scale + split
    ├── train_mlflow.py         ← Stage 3: train + MLflow logging
    ├── evaluate.py             ← Stage 4: leaderboard + run detail
    ├── pipeline_runner.py      ← Orchestrator: runs all 4 stages
    └── ml_pipeline.py          ← Original simple pipeline (pre-MLOps)

.github/copilot/skills/
    ├── validate-data.md        ← NEW
    ├── train-model.md          ← NEW
    ├── evaluate-model.md       ← NEW
    ├── explore-dataset.md
    ├── setup-env.md
    └── explain-notebook.md

mlruns/                         ← MLflow tracking data (git-ignored)
```
