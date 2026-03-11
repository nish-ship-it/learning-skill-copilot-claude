# Learning GitHub Copilot CLI Skills
### A hands-on guide for data & ML teams

> **What this is:** A step-by-step learning repository for creating, using, and sharing custom GitHub Copilot CLI skills — illustrated with real Python/ML examples you can run today.

---

## Why this repo exists

GitHub Copilot CLI can be extended with **skills** — focused instruction sets that teach Copilot how to handle specific tasks in your project. Once defined, any team member with Copilot access gets the same expert help automatically.

This repo teaches you to go from zero to a full skill-sharing workflow, documented so you can adapt it for your own team or org.

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

---

## Example skills (ready to use)

All three skills live in [`.github/copilot/skills/`](.github/copilot/skills/) and are active in this repo automatically.

| Skill | File | What it does |
|-------|------|--------------|
| `explore-dataset` | [explore-dataset.md](.github/copilot/skills/explore-dataset.md) | Runs EDA on a CSV: shape, dtypes, nulls, distributions |
| `setup-env` | [setup-env.md](.github/copilot/skills/setup-env.md) | Sets up a Python venv with the right dependencies |
| `explain-notebook` | [explain-notebook.md](.github/copilot/skills/explain-notebook.md) | Summarises what a Jupyter notebook does and suggests improvements |

---

## Repository structure

```
.
├── docs/                    # Learning guides (read in order)
├── .github/
│   ├── copilot-instructions.md   # Project context for every Copilot session
│   └── copilot/skills/           # Custom skill definitions
├── examples/
│   ├── data/sample.csv           # Sample dataset to practise with
│   ├── notebooks/eda_demo.ipynb  # Demo EDA notebook
│   └── src/ml_pipeline.py        # Simple ML pipeline
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
