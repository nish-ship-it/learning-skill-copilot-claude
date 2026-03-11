# Skill Workflow Run — 2026-03-11

> **What this is:** A captured end-to-end run of all three project skills against the example ML project.
> Use this as a reference to understand what each skill produces, or as a demo for your org.
>
> **Dataset:** `examples/data/sample.csv` — 25-row income prediction dataset
> **Environment:** Python 3.12.3, pandas 2.2.2, scikit-learn 1.4.2
> **Run date:** 2026-03-11 06:54 UTC

---

## How this run was triggered

Each skill was invoked by typing a natural language prompt into a `copilot` session
launched from the repo root. The `copilot` agent matched the prompt to the correct
skill via its `description:` field and followed the skill's instructions.

```bash
cd learning-skill-copilot-claude
copilot
# Then inside the session:
# > set up the Python environment for this project
# > explore examples/data/sample.csv, target column is income_bracket
# > explain what examples/notebooks/eda_demo.ipynb does
# > run examples/src/ml_pipeline.py
```

---

## Skill 1 — `setup-env`

**Skill file:** [`.github/copilot/skills/setup-env.md`](../.github/copilot/skills/setup-env.md)
**Prompt used:** `set up the Python environment for this project`

### Output

```
✅ venv created at .venv/

Python 3.12.3

Name: pandas          Version: 2.2.2
Name: scikit-learn    Version: 1.4.2
Name: jupyter         Version: 1.0.0

✅ All packages verified
```

### What the skill did

1. Created `.venv/` with `python3 -m venv .venv`
2. Activated the environment
3. Upgraded pip, then installed all packages from `requirements.txt`
4. Verified imports: `pandas`, `sklearn`, `matplotlib`, `seaborn`

---

## Skill 2 — `explore-dataset`

**Skill file:** [`.github/copilot/skills/explore-dataset.md`](../.github/copilot/skills/explore-dataset.md)
**Prompt used:** `explore examples/data/sample.csv, target column is income_bracket`

### Output

```
============================================================
EXPLORE-DATASET SKILL — running on: examples/data/sample.csv
============================================================

📐 Shape: 25 rows × 6 columns

📋 Columns & dtypes:
   age                  int64
   income               int64
   education_years      int64
   hours_per_week       int64
   occupation           object
   income_bracket       object

💾 Memory usage: 3.6 KB

🔍 Missing values:
   ✅ No missing values

📊 Numeric stats:
             age         income  education_years  hours_per_week
count  25.000000      25.000000        25.000000       25.000000
mean   37.440000   63400.000000        14.600000       44.000000
std    10.508251   27192.217024         1.825742        6.557439
min    22.000000   28000.000000        12.000000       35.000000
25%    29.000000   41000.000000        13.000000       40.000000
50%    36.000000   58000.000000        14.000000       42.000000
75%    45.000000   85000.000000        16.000000       48.000000
max    61.000000  120000.000000        18.000000       60.000000

📊 Categorical stats:
       occupation income_bracket
count          25             25
unique          6              2
top          Tech           >50K
freq            6             13

🎯 Target column 'income_bracket' distribution:
   >50K        13 (52%)  ███████████████
   <=50K       12 (48%)  ██████████████

🔗 Correlation matrix (numeric columns):
                  age  income  education_years  hours_per_week
age              1.00    0.88             0.78            0.65
income           0.88    1.00             0.95            0.90
education_years  0.78    0.95             1.00            0.91
hours_per_week   0.65    0.90             0.91            1.00

⚠️  High correlations (|r| > 0.7):
   age ↔ income: 0.88
   age ↔ education_years: 0.78
   income ↔ education_years: 0.95
   income ↔ hours_per_week: 0.90
   education_years ↔ hours_per_week: 0.91

💡 Recommendations:
   1. Dataset is clean — no missing values. Ready for preprocessing.
   2. 'income' and 'hours_per_week' are numeric and span wide ranges
      — consider scaling before ML.
   3. 'occupation' is categorical with 6 unique values
      — use LabelEncoder or OneHotEncoder.
   4. Target is balanced enough for classification (see distribution above).
============================================================
```

### Key findings

| Finding | Detail |
|---------|--------|
| Data quality | ✅ Zero missing values |
| Target balance | 52% `>50K` / 48% `<=50K` — well balanced |
| Multicollinearity | ⚠️ `income ↔ education_years` r=0.95, `income ↔ hours_per_week` r=0.90 |
| Preprocessing needed | Scale numerics, encode `occupation` |

---

## Skill 3 — `explain-notebook`

**Skill file:** [`.github/copilot/skills/explain-notebook.md`](../.github/copilot/skills/explain-notebook.md)
**Prompt used:** `explain what examples/notebooks/eda_demo.ipynb does`

### Output

```
============================================================
EXPLAIN-NOTEBOOK SKILL — examples/notebooks/eda_demo.ipynb
============================================================

📄 SUMMARY
This notebook performs exploratory data analysis on
examples/data/sample.csv — a 25-row income prediction dataset.
It loads the data with pandas, inspects shape/dtypes, checks for
missing values, visualises the target column distribution, plots
numeric feature histograms, and produces a correlation heatmap.
Output: a series of matplotlib/seaborn charts, no model is trained.

🔬 CELL-BY-CELL BREAKDOWN

  Cell 1 — Imports
  Code:  import pandas as pd...
  Note:  Loads pandas, matplotlib, seaborn. Sets seaborn whitegrid
         theme. Safe.

  Cell 2 — Load & inspect
  Code:  df = pd.read_csv('../../examples/data/sample.csv')...
  Note:  Reads sample.csv via relative path. ⚠️ Will break if notebook
         is moved or run from a different working directory.

  Cell 3 — df.info()
  Code:  df.info()...
  Note:  Prints column dtypes and non-null counts. Good sanity check.

  Cell 4 — df.describe()
  Code:  df.describe()...
  Note:  Numeric summary stats. No issues.

  Cell 5 — Missing values
  Code:  missing = df.isnull().sum()...
  Note:  Checks for nulls and prints a message if none found.
         Correct pattern.

  Cell 6 — Target distribution
  Code:  ax = df['income_bracket'].value_counts().plot(kind='bar'...
  Note:  Bar chart of income_bracket. Hardcodes column name — would
         need updating for a different dataset.

  Cell 7 — Numeric histograms
  Code:  numeric_cols = df.select_dtypes(include='number')...
  Note:  Uses select_dtypes — adapts automatically to new columns.
         Good pattern.

  Cell 8 — Correlation heatmap
  Code:  corr = df[numeric_cols].corr()...
  Note:  Seaborn heatmap of numeric correlations. No random state
         needed here.

⚠️  ISSUES FOUND

  1. Hardcoded relative path
     '../../examples/data/sample.csv' breaks if notebook is run from
     anywhere other than examples/notebooks/.
     Fix: define DATA_PATH at the top of the notebook.

  2. Hardcoded column name
     'income_bracket' is hardcoded in Cell 6.
     Fix: define TARGET = 'income_bracket' in the first cell.

  3. No markdown explaining the correlation heatmap
     A reader won't know what to look for without context.
     Fix: add a markdown cell above it.

💡 TOP 3 IMPROVEMENTS

  1. Extract config to a top cell (highest impact)
     Define DATA_PATH and TARGET at the top. Makes the notebook
     reusable on any similar dataset with a one-line change.

  2. Add markdown narrative between sections
     Turns the notebook from a script into a shareable report.

  3. Add a summary cell at the end
     A final markdown cell with key findings makes the notebook
     self-contained for readers who only see the output.
============================================================
```

---

## Step 4 — ML Pipeline (end-to-end)

**Script:** `examples/src/ml_pipeline.py`
**Command:** `python examples/src/ml_pipeline.py`

This is not a skill file — it's the actual Python pipeline the skills helped prepare and review. Running it completes the full workflow loop.

### Output

```
Loaded 25 rows, 6 columns

Accuracy: 80.00%

              precision    recall  f1-score   support

       <=50K       0.67      1.00      0.80         2
        >50K       1.00      0.67      0.80         3

    accuracy                           0.80         5
   macro avg       0.83      0.83      0.80         5
weighted avg       0.87      0.80      0.80         5
```

### Results interpretation

| Metric | Value | Notes |
|--------|-------|-------|
| Accuracy | 80% | On 5-row test split — treat as directional only |
| `>50K` precision | 1.00 | No false positives for high earners |
| `<=50K` recall | 1.00 | Correctly identified all low earners |
| Main weakness | `>50K` recall 0.67 | 1 high earner misclassified as low |

> ⚠️ 25 rows is intentionally tiny for learning purposes. In a real project the explore-dataset skill would flag this sample size as insufficient for reliable evaluation.

---

## What this run demonstrates

1. **Skills produce consistent, structured output** — every teammate running `explore-dataset` on the same file gets the same 7-section report.
2. **Skills catch real issues** — the `explain-notebook` skill found 3 genuine problems in the demo notebook (hardcoded path, hardcoded column name, missing narrative).
3. **The workflow is learnable** — each skill's output maps directly back to its instruction file, so you can read the skill, predict the output, and verify.

---

## Reproducing this run

```bash
git clone https://github.com/nish-ship-it/learning-skill-copilot-claude
cd learning-skill-copilot-claude
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python examples/src/ml_pipeline.py
```

To run with the full skill experience, launch the `copilot` agent and use the natural language prompts shown at the top of this document.
