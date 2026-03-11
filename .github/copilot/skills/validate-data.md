---
name: validate-data
description: >
  Validate a dataset before training. Use when the user says:
  "validate my data", "check data quality", "run data validation",
  "is my CSV ready for training", "check for nulls and errors",
  "Stage 1 data validation", "validate sample.csv".
---

# validate-data skill

Run **Stage 1: Data Validation** to check whether a dataset is ready for training.

## What to do

1. Identify the CSV path from context (default: `examples/data/sample.csv`).
2. Run the validation script:

```bash
python examples/src/data_validation.py examples/data/sample.csv
```

3. Interpret the output:
   - **Passed ✓** — safe to proceed to preprocessing and training.
   - **Failed ✗** — list the errors and explain what must be fixed.
   - For each **Warning**, explain its impact (e.g., missing values will be imputed; class imbalance will be handled via `class_weight='balanced'`).

## Checks performed

| Check | Threshold | Action if failed |
|---|---|---|
| Missing columns | Any required col absent | Pipeline aborted |
| Null rate per column | > 20% nulls | Pipeline aborted |
| Target value validity | Values outside {`>50K`, `<=50K`} | Pipeline aborted |
| Null rate 1–20% | Warning only | Rows will be median-imputed |
| Class imbalance < 10% minority | Warning only | Use `class_weight='balanced'` |

## After validation

If validation **passed**, tell the user:
> "Data validation passed. You can now run the full pipeline with:
> `python examples/src/pipeline_runner.py`"

If validation **failed**, tell the user which specific errors to fix and re-validate.

## Tips for the user

- Validation runs automatically as the first step of `pipeline_runner.py` — you don't need to run it separately unless debugging data issues.
- Add a new column? Update `SCHEMA` in `examples/src/data_validation.py`.
- Want stricter null tolerance? Lower `MAX_NULL_RATE` in that same file.
