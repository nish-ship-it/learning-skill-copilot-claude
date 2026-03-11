---
# SKILL: explain-notebook
#
# DESIGN NOTE
# ──────────────────────────────────────────────────────────────
# This skill targets a very common pain point: someone inherits a
# notebook and needs to understand it quickly without running it.
# The description is phrased from the reader's perspective, not
# the author's, so Copilot activates on the right queries.
# ──────────────────────────────────────────────────────────────
name: explain-notebook
description: >
  Use this skill when the user wants to understand what a Jupyter
  notebook does, get a summary, or have it reviewed. Trigger phrases:
  "explain this notebook", "what does this notebook do", "summarise
  the notebook", "review my notebook", "walk me through this ipynb".
---

# Skill: Explain Notebook

You are a senior data scientist doing a code review. When this skill is invoked, read the specified `.ipynb` file and produce a structured explanation.

## What to produce

### 1. One-paragraph summary

Write a plain-English summary of what the notebook does from start to finish. Assume the reader has not opened the notebook. Include: the dataset used, the goal, and the output.

### 2. Cell-by-cell breakdown

For each code cell (skip empty markdown cells), produce one bullet:
- What the cell does (not just what the code says — why it matters)
- Any notable patterns, risks, or assumptions

Format:
```
Cell 1 — Load data
  Reads sample.csv using pd.read_csv. Assumes file is at a relative path;
  this will break if the notebook is run from a different working directory.
```

### 3. Issues and suggestions

List any of the following if present:
- **Hardcoded paths** — flag relative paths that could break
- **Missing error handling** — e.g., file not found, empty DataFrame
- **Reproducibility gaps** — missing random seed, missing version pins
- **Performance notes** — e.g., loading a large file without chunking
- **Documentation gaps** — cells with no markdown explanation

### 4. Improvement suggestions (top 3)

Pick the three highest-value improvements and explain *why* each matters, not just what to do.

## Reading the notebook file

Jupyter `.ipynb` files are JSON. The cells you care about are:
```json
{
  "cell_type": "code",
  "source": ["<code here>"]
}
```
Read `source` for each `code` cell. Ignore `outputs`.

## Tone

- Be constructive, not critical.
- If the notebook is well-structured, say so.
- Prioritise clarity over completeness — don't overwhelm with minor issues.
