# Learning GitHub Copilot CLI Skills
### A hands-on guide for data & ML teams

> **What this is:** A step-by-step learning repository for creating, using, and sharing custom GitHub Copilot CLI skills — illustrated with real Python/ML examples you can run today.

---

## Why this repo exists

GitHub Copilot CLI can be extended with **skills** — focused instruction sets that teach Copilot how to handle specific tasks in your project. Once defined, any team member with Copilot access gets the same expert help automatically.

This repo teaches you to go from zero to a full skill-sharing workflow, documented so you can adapt it for your own team or org.

---

## ⚠️ Two tools, one name — know the difference

| Tool | Command | Skills support |
|------|---------|---------------|
| `gh copilot suggest` / `gh copilot explain` | Shell command helper | ❌ No skill system |
| **`copilot`** (Copilot CLI agent) | Full agentic assistant in your terminal | ✅ Reads `.github/copilot/skills/` automatically |

**The skills in this repo only work with the `copilot` agent.** Install it:
```bash
curl -fsSL https://gh.io/copilot-install | bash
# or: brew install copilot-cli
# or: npm install -g @github/copilot
```

Then launch it in this project with `copilot`. Use `/skills` inside the session to confirm skills are loaded. See [docs/05-using-skills-in-cli.md](docs/05-using-skills-in-cli.md) for the full mechanics.

---

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_ORG/learning-skill-copilot-claude
cd learning-skill-copilot-claude

# 2. Set up the Python environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Open the learning docs in order (start here)
# docs/00-overview.md
```

---

## Learning path

| Step | Document | What you'll learn |
|------|----------|-------------------|
| 0 | [docs/00-overview.md](docs/00-overview.md) | What skills are and how the CLI uses them |
| 1 | [docs/01-creating-first-skill.md](docs/01-creating-first-skill.md) | Create and invoke your first skill |
| 2 | [docs/02-skill-anatomy.md](docs/02-skill-anatomy.md) | Every part of a skill file explained |
| 3 | [docs/03-ml-data-skills.md](docs/03-ml-data-skills.md) | Skills for pandas, scikit-learn, and notebooks |
| 4 | [docs/04-sharing-across-org.md](docs/04-sharing-across-org.md) | Share skills across your GitHub org |
| 5 | [docs/05-using-skills-in-cli.md](docs/05-using-skills-in-cli.md) | How to actually invoke skills in a `copilot` session |
| 6 | [docs/06-mlops-with-skills.md](docs/06-mlops-with-skills.md) | MLOps pipeline with MLflow + 3 new skills |

## Example run output

| Run | File | Description |
|-----|------|-------------|
| Skill workflow | [`docs/runs/2026-03-11-workflow-run.md`](docs/runs/2026-03-11-workflow-run.md) | All 3 original skills executed end-to-end |
| MLOps pipeline | [`docs/runs/2026-03-11-mlops-run.md`](docs/runs/2026-03-11-mlops-run.md) | Full 4-stage MLOps run with 2 MLflow experiments compared |

---

## Example skills (ready to use)

All six skills live in [`.github/copilot/skills/`](.github/copilot/skills/) and are active in this repo automatically.

| Skill | File | What it does |
|-------|------|--------------|
| `explore-dataset` | [explore-dataset.md](.github/copilot/skills/explore-dataset.md) | EDA: shape, dtypes, nulls, distributions, correlations |
| `setup-env` | [setup-env.md](.github/copilot/skills/setup-env.md) | Sets up a Python venv with the right dependencies |
| `explain-notebook` | [explain-notebook.md](.github/copilot/skills/explain-notebook.md) | Summarises and reviews a Jupyter notebook |
| `validate-data` | [validate-data.md](.github/copilot/skills/validate-data.md) | Validates CSV before training (schema, nulls, balance) |
| `train-model` | [train-model.md](.github/copilot/skills/train-model.md) | Runs full MLOps pipeline with MLflow tracking |
| `evaluate-model` | [evaluate-model.md](.github/copilot/skills/evaluate-model.md) | Compares runs, shows leaderboard, identifies best model |

---

## Repository structure

```
.
├── docs/                    # Learning guides (read in order: 00 → 06)
│   └── runs/                # Captured pipeline run outputs
├── .github/
│   ├── copilot-instructions.md   # Project context for every Copilot session
│   └── copilot/skills/           # 6 custom skill definitions
├── examples/
│   ├── data/sample.csv           # 220-row dataset (9 features, missing values)
│   ├── notebooks/eda_demo.ipynb  # Demo EDA notebook (fully executed)
│   └── src/
│       ├── data_validation.py    # Stage 1: validate
│       ├── preprocessing.py      # Stage 2: impute/encode/scale
│       ├── train_mlflow.py       # Stage 3: train + MLflow
│       ├── evaluate.py           # Stage 4: leaderboard
│       ├── pipeline_runner.py    # Orchestrator
│       └── ml_pipeline.py        # Original simple pipeline
└── requirements.txt
```

---

## Dataset: what's in `examples/data/sample.csv`

The dataset simulates an **income-bracket prediction** problem — a classic ML task with real-world complexity baked in.

| Property | Value |
|---|---|
| Rows | 220 |
| Features | 9 (8 input + 1 target) |
| Target | `income_bracket` — `>50K` or `<=50K` |
| Class balance | 63% `<=50K` / 37% `>50K` (mild imbalance) |
| Missing values | `age`: 5 nulls · `hours_per_week`: 7 nulls |

### Columns

| Column | Type | Notes |
|---|---|---|
| `age` | numeric (float) | 18–75, **5 missing** → median-imputed |
| `income` | numeric (int) | Annual income in $, 15k–140k |
| `education_years` | numeric (int) | Years of formal education, 6–20 |
| `hours_per_week` | numeric (float) | Weekly work hours, 20–80, **7 missing** → median-imputed |
| `occupation` | categorical | Tech, Sales, Service, Admin, Professional, Craft, Transport, Other |
| `marital_status` | categorical | Married, Single, Divorced, Widowed, Separated |
| `gender` | categorical | Male, Female |
| `native_country` | categorical | United-States (60%), Mexico, Philippines, Germany, Canada, India, Other |
| `income_bracket` | target | `>50K` or `<=50K` |

### How it evolved

| | Original (v1) | Current (v2) |
|---|---|---|
| Rows | 25 | **220** |
| Columns | 6 | **9** |
| Missing values | None | **12 cells** (age + hours_per_week) |
| Class balance | 52/48% (balanced) | **63/37%** (imbalanced) |
| New features | — | `marital_status`, `gender`, `native_country` |

The added complexity drives real MLOps requirements: imputation, class-weighted training, F1 over accuracy, and schema validation before every run. See [docs/06-mlops-with-skills.md](docs/06-mlops-with-skills.md) for how the pipeline handles each one.

---

## Prerequisites

- GitHub account with [Copilot Individual or Business](https://github.com/features/copilot)
- `gh` CLI installed: [cli.github.com](https://cli.github.com)
- Python 3.9+

---

## Contributing / adapting for your org

See [docs/04-sharing-across-org.md](docs/04-sharing-across-org.md) for how to fork this repo, customise the skills for your team's stack, and roll it out.

MIT License — use freely, attribution appreciated.
