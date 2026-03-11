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

## Prerequisites

- GitHub account with [Copilot Individual or Business](https://github.com/features/copilot)
- `gh` CLI installed: [cli.github.com](https://cli.github.com)
- Python 3.9+

---

## Contributing / adapting for your org

See [docs/04-sharing-across-org.md](docs/04-sharing-across-org.md) for how to fork this repo, customise the skills for your team's stack, and roll it out.

MIT License — use freely, attribution appreciated.
