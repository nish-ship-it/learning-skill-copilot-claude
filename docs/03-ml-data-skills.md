# 03 — Skills for ML and Data Science Workflows

This guide covers patterns specific to Python data/ML projects. The skills in `.github/copilot/skills/` in this repo implement these patterns — read them alongside this doc.

---

## The ML workflow map

```
Raw data → EDA → Preprocessing → Training → Evaluation → Deployment
   ↑           ↑           ↑           ↑           ↑
explore-dataset  (you build)  (you build)  (you build)  (you build)
```

This repo ships with `explore-dataset` for the first stage. The others are left as exercises — building them is how you learn.

---

## Pattern 1: Dataset exploration skill

**The key insight:** EDA always involves the same 6 steps, but generic Copilot doesn't know your column names or target variable. A skill can encode your team's standard EDA checklist.

**What to include in an EDA skill body:**
- Load → profile → nulls → distributions → correlations → target analysis
- Explicit output format (so everyone gets the same EDA report structure)
- Your team's standard null-handling rules (e.g., "flag if >10% missing")

See: [`.github/copilot/skills/explore-dataset.md`](../.github/copilot/skills/explore-dataset.md)

---

## Pattern 2: Preprocessing skill

A preprocessing skill is useful when your team uses the same pipeline across projects. Example body structure:

```markdown
---
name: preprocess-data
description: >
  Use this skill when the user needs to preprocess a dataset for ML.
  Trigger phrases: "preprocess the data", "encode features",
  "handle missing values", "prepare data for training", "feature engineering".
---

# Skill: Preprocess Data

You are a data engineer. When invoked:

1. Identify numeric vs. categorical columns
2. For numerics: impute median, scale with StandardScaler
3. For categoricals: impute mode, encode with LabelEncoder or OneHotEncoder
4. Print shape before and after preprocessing
5. Save the processed DataFrame to `data/processed/` with `_processed` suffix

Always use sklearn Pipeline to chain steps. Never modify the raw data file.
```

---

## Pattern 3: Model training skill

Encode your team's standard experiment tracking and evaluation format:

```markdown
---
name: train-model
description: >
  Use this skill to train a model. Trigger phrases: "train a model",
  "fit the data", "run the pipeline", "classification", "regression".
---

# Skill: Train Model

You are an ML engineer. When invoked:

1. Split data 80/20 train/test with random_state=42
2. Train a RandomForestClassifier with n_estimators=100 as the baseline
3. Print: accuracy, precision, recall, F1 (weighted)
4. Print feature importances sorted descending
5. Save the model to `models/` with a timestamp in the filename

Always set random_state=42 for reproducibility.
Always print the training data shape before fitting.
```

---

## Pattern 4: Notebook explanation skill

Notebooks are the hardest artefacts to hand off. An `explain-notebook` skill ensures anyone can understand a notebook without running it.

See: [`.github/copilot/skills/explain-notebook.md`](../.github/copilot/skills/explain-notebook.md)

**Extra tip:** Add a `review-notebook` variant that specifically looks for reproducibility issues — hardcoded paths, missing seeds, undocumented magic numbers.

---

## Pattern 5: Environment setup skill

Every new team member spends time on environment setup. A skill eliminates this:

See: [`.github/copilot/skills/setup-env.md`](../.github/copilot/skills/setup-env.md)

---

## Composing skills: one task, multiple skills

For complex workflows, resist the urge to put everything in one skill. Instead, create a chain:

```
User: "Run the full ML pipeline on sample.csv"

Copilot activates:
  1. explore-dataset  → EDA report
  2. preprocess-data  → cleaned data
  3. train-model      → trained model + metrics
```

This only works if each skill's description is distinct enough that Copilot picks the right one at each step. The user may need to invoke them sequentially rather than all at once.

---

## Naming convention for ML skills

| Skill type | Naming pattern | Example |
|------------|---------------|---------|
| Data operation | `verb-noun` | `explore-dataset`, `clean-data` |
| ML stage | `verb-noun` | `train-model`, `evaluate-model` |
| Environment | `noun-action` | `setup-env`, `check-deps` |
| Explanation | `explain-noun` | `explain-notebook`, `explain-pipeline` |

---

## Exercise: build the preprocessing skill

1. Copy the template from Pattern 2 above
2. Save it to `.github/copilot/skills/preprocess-data.md`
3. Adjust the instructions to match your team's actual preprocessing steps
4. Test it on `examples/data/sample.csv`
5. Commit and share with your team

→ [04-sharing-across-org.md](04-sharing-across-org.md) — how to share what you've built
