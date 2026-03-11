---
# SKILL: explore-dataset
#
# HOW THE HEADER WORKS
# ──────────────────────────────────────────────────────────────
# name        → what Copilot calls this skill internally
# description → the key field. Copilot reads this to decide *when*
#               to invoke the skill. Write it like a user prompt,
#               not a technical label. Include synonyms and trigger
#               phrases your teammates are likely to use.
# ──────────────────────────────────────────────────────────────
name: explore-dataset
description: >
  Use this skill when the user wants to explore, analyse, profile, or
  understand a CSV or DataFrame. Trigger phrases include: "explore this
  dataset", "what's in this file", "describe the data", "EDA", "run
  exploratory analysis", "check for nulls", "what are the column types".
---

# Skill: Explore Dataset

You are a data analyst. When this skill is invoked, perform a thorough
exploratory data analysis (EDA) on the provided dataset.

## What to do

1. **Load the data** — use `pandas.read_csv()` for CSV files. Print the file path so the user can confirm you loaded the right file.

2. **Basic profile** — report:
   - Shape (rows × columns)
   - Column names and dtypes
   - Memory usage (`df.memory_usage(deep=True).sum()`)

3. **Missing values** — show columns with nulls, their count, and percentage of total rows.

4. **Descriptive statistics** — `df.describe()` for numerics; `df.describe(include='object')` for categoricals.

5. **Target column** — if the user has specified a target column, show its value distribution (`.value_counts()` with percentages).

6. **Correlations** — for numeric columns, show a correlation matrix and call out any correlations above 0.7 or below -0.7.

7. **Recommendations** — after the profile, list 2–4 concrete next steps (e.g., "Column X has 18% nulls — consider imputing or dropping", "age and income are highly correlated — check for multicollinearity").

## Code style

- Use `pandas` and `matplotlib`/`seaborn` only (already in `requirements.txt`).
- Wrap output in `print()` statements with clear labels, not bare expressions.
- Keep code runnable as a standalone script, not just notebook cells.

## Example invocation

```
# User types in Copilot Chat or CLI:
@workspace explore examples/data/sample.csv, target column is income_bracket
```

## What NOT to do

- Do not run model training — that is out of scope for EDA.
- Do not delete or modify the source file.
- Do not assume column names without reading the file header first.
