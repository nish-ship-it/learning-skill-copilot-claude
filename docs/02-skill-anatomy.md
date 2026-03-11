# 02 — Skill Anatomy: Every Part Explained

A skill file has two sections: **front matter** (YAML) and **body** (markdown). Here is a fully annotated example.

---

## Full annotated example

```markdown
---
name: explore-dataset          # (1) Internal name — kebab-case, no spaces
description: >                 # (2) Activation phrase — the most important field
  Use this skill when the user wants to explore, analyse, profile, or
  understand a CSV or DataFrame. Trigger phrases include: "explore this
  dataset", "what's in this file", "describe the data", "EDA", "run
  exploratory analysis", "check for nulls", "what are the column types".
---

# Skill: Explore Dataset       # (3) Body — free-form markdown instructions

You are a data analyst. When this skill is invoked, perform a thorough
exploratory data analysis (EDA) on the provided dataset.

## What to do
...
```

---

## Field reference

### `name` (required)

```yaml
name: explore-dataset
```

- Used internally by Copilot for logging and disambiguation
- Must be unique within the repo
- Convention: kebab-case, descriptive, matches the filename

---

### `description` (required — most important)

```yaml
description: >
  Use this skill when the user wants to explore a CSV or DataFrame.
  Trigger phrases: "EDA", "explore the data", "what's in this file".
```

**This is the only field Copilot uses to decide whether to activate your skill.**

Rules for good descriptions:
1. Start with `Use this skill when...` — tells Copilot the activation condition
2. List synonyms and trigger phrases explicitly
3. Cover the vocabulary your teammates actually use, not just technical terms
4. Make it distinct from other skills — if two descriptions overlap, Copilot may pick the wrong one

The `>` after `description:` is YAML "block scalar" — it lets you write a multi-line string cleanly.

---

### Body (required)

Everything after the closing `---` is the skill body. Copilot reads this as its instruction set when the skill is active.

**Effective body patterns:**

| Pattern | Example |
|---------|---------|
| Role assignment | `You are a senior data scientist...` |
| Numbered steps | `1. Load the data\n2. Check for nulls\n3. Summarise...` |
| Code style rules | `Use pandas only. Wrap output in print() with clear labels.` |
| Explicit exclusions | `Do NOT run model training. Do NOT modify the source file.` |
| Example invocation | Show what a good user prompt looks like |

**Why explicit exclusions matter:** Without them, Copilot may try to be helpful and go beyond scope. A `## What NOT to do` section keeps the skill focused.

---

## Skill scoping

| Scope | Location | Who sees it |
|-------|----------|-------------|
| Project | `.github/copilot/skills/*.md` | Everyone who clones the repo |
| Personal | `~/.config/github-copilot/skills/*.md` | Only you, across all repos |

For team sharing, always use project scope.

---

## File naming

| Convention | Example |
|------------|---------|
| One skill per file | `explore-dataset.md` |
| Name matches `name` field | `name: explore-dataset` → `explore-dataset.md` |
| Kebab-case | `run-notebook.md` not `runNotebook.md` |

---

## Common mistakes

| Mistake | Effect | Fix |
|---------|--------|-----|
| Missing front matter `---` delimiters | Copilot ignores the file | Add opening and closing `---` |
| Vague description | Wrong skill activates | Add specific trigger phrases |
| No role assignment in body | Generic responses | Add `You are a [role]...` at the top |
| Overlapping descriptions | Inconsistent activation | Make each skill's triggers distinct |
| Body is too long and unfocused | Copilot follows some steps but not others | Split into multiple focused skills |

---

→ [03-ml-data-skills.md](03-ml-data-skills.md) — applying these patterns to pandas and scikit-learn workflows
