# Copilot Instructions

## Purpose

Learning and reference repository for building, managing, and sharing GitHub Copilot CLI skills in ML/data analytics projects. Intended for org-wide knowledge sharing. Stack: Python, pandas, scikit-learn, Jupyter.

## Commands

```bash
# Environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the example ML pipeline
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
docs/                     ← step-by-step learning guides (00 through 04)
examples/
  data/sample.csv         ← 25-row income prediction dataset
  notebooks/eda_demo.ipynb
  src/ml_pipeline.py      ← load → preprocess → train → evaluate pipeline
requirements.txt          ← pandas 2.2.2, scikit-learn 1.4.2, jupyter, matplotlib, seaborn
```

The example ML pipeline in `examples/src/ml_pipeline.py` follows a strict functional structure: `load_data` → `preprocess` → `train` → `evaluate` → `main`. When adding to it, keep this separation.

## Skills in this repo

| Skill file | Activates when user asks about |
|-----------|-------------------------------|
| `explore-dataset.md` | EDA, dataset profiling, nulls, distributions, correlations |
| `setup-env.md` | Python env setup, venv creation, installing requirements |
| `explain-notebook.md` | What a notebook does, notebook review, summarising `.ipynb` |

## Conventions

- **Skill files:** Markdown with YAML front matter. Location: `.github/copilot/skills/`. Named in kebab-case matching the `name:` field. One skill per file. Every skill must have `name:` and `description:` fields.
- **Skill `description:` field:** Written as `Use this skill when...` followed by explicit trigger phrases. This is how Copilot decides which skill to activate — write it from the user's vocabulary, not the author's.
- **Python code style:** Type hints on all function signatures. Constants in `UPPER_SNAKE_CASE` at module level. Functions follow the verb-noun pattern (`load_data`, `train_model`).
- **Docs:** Written for a reader who has not read any other file in the repo. Each doc ends with a `→ Next step` link.
- **Sharing pattern:** Copy skill files into other repos to share. Do not use symlinks. Customise after copying — don't import skills as-is without reviewing them for your project's conventions.
