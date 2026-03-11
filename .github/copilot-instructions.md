# Copilot Instructions

## Purpose

Learning and reference repository for building, managing, and sharing GitHub Copilot CLI skills in ML/data analytics projects. Intended for org-wide knowledge sharing. Stack: Python, pandas, scikit-learn, Jupyter, MLflow.

## Commands

```bash
# Environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# MLOps pipeline (full 4-stage run with MLflow tracking)
python examples/src/pipeline_runner.py                            # default params
python examples/src/pipeline_runner.py examples/data/sample.csv \
  --n-estimators 200 --max-depth 8 --run-name my-run             # custom params

# Individual pipeline stages
python examples/src/data_validation.py examples/data/sample.csv  # Stage 1: validate
python examples/src/train_mlflow.py examples/data/sample.csv     # Stage 3: train + log
python examples/src/evaluate.py                                   # Stage 4: leaderboard

# MLflow UI
mlflow ui --port 5000   # then open http://127.0.0.1:5000

# Original simple pipeline (pre-MLOps reference)
python examples/src/ml_pipeline.py

# Launch the example notebook
jupyter notebook examples/notebooks/eda_demo.ipynb

# Copilot CLI
gh copilot suggest "<task in plain English>"   # get a shell command
gh copilot explain "<shell command>"           # explain a command
```

## Architecture

```
.github/copilot/skills/   ← project-scoped skill definitions (one .md per skill)
.github/copilot-instructions.md  ← this file (project context for all sessions)
docs/                     ← step-by-step learning guides (00 through 06)
docs/runs/                ← captured output from each pipeline run
examples/
  data/sample.csv         ← 220-row income prediction dataset (9 features)
  notebooks/eda_demo.ipynb
  src/
    data_validation.py    ← Stage 1: schema/null/balance checks
    preprocessing.py      ← Stage 2: impute → encode → scale → split
    train_mlflow.py       ← Stage 3: train RandomForest + log to MLflow
    evaluate.py           ← Stage 4: compare runs, leaderboard
    pipeline_runner.py    ← Orchestrator: runs all 4 stages in sequence
    ml_pipeline.py        ← Original simple pipeline (pre-MLOps reference)
mlruns/                   ← MLflow tracking data (git-ignored, local only)
requirements.txt          ← pandas, scikit-learn, jupyter, matplotlib, seaborn, mlflow
```

**Pipeline flow:** `data_validation` → `preprocessing` → `train_mlflow` → `evaluate`  
The orchestrator `pipeline_runner.py` accepts `--n-estimators`, `--max-depth`, and `--run-name` flags to support multi-run experiments.

## Skills in this repo

| Skill file | Activates when user asks about |
|-----------|-------------------------------|
| `explore-dataset.md` | EDA, dataset profiling, nulls, distributions, correlations |
| `setup-env.md` | Python env setup, venv creation, installing requirements |
| `explain-notebook.md` | What a notebook does, notebook review, summarising `.ipynb` |
| `validate-data.md` | Data validation, check data quality, is my CSV ready for training |
| `train-model.md` | Train the model, run the ML pipeline, start an MLflow experiment |
| `evaluate-model.md` | Compare runs, show leaderboard, which hyperparameters worked best |

## Conventions

- **Skill files:** Markdown with YAML front matter. Location: `.github/copilot/skills/`. Named in kebab-case matching the `name:` field. One skill per file. Every skill must have `name:` and `description:` fields.
- **Skill `description:` field:** Written as `Use this skill when...` followed by explicit trigger phrases. This is how Copilot decides which skill to activate — write it from the user's vocabulary, not the author's.
- **Python code style:** Type hints on all function signatures. Constants in `UPPER_SNAKE_CASE` at module level. Functions follow the verb-noun pattern (`load_data`, `train_model`).
- **Docs:** Written for a reader who has not read any other file in the repo. Each doc ends with a `→ Next step` link.
- **Sharing pattern:** Copy skill files into other repos to share. Do not use symlinks. Customise after copying — don't import skills as-is without reviewing them for your project's conventions.
