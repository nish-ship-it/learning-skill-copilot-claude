# 01 — Creating Your First Skill

> **Goal:** Create a working skill from scratch, invoke it, and iterate on it. This takes ~10 minutes.

## Prerequisites

- [ ] `gh` CLI installed and authenticated (`gh auth login`)
- [ ] GitHub Copilot enabled on your account
- [ ] This repo cloned locally

---

## Step 1: Create the skills directory

```bash
mkdir -p .github/copilot/skills
```

This is the only location Copilot looks for project skills. The path must be exact.

---

## Step 2: Create a skill file

Create `.github/copilot/skills/my-first-skill.md`:

```markdown
---
name: my-first-skill
description: >
  Use this skill when the user asks about the Python environment,
  installed packages, or Python version in this project.
---

# Skill: Python Environment Info

When invoked, check and report:
1. Python version: `python --version`
2. Active virtual environment (check $VIRTUAL_ENV)
3. Installed packages relevant to this project: pandas, scikit-learn, jupyter
4. Whether requirements.txt dependencies are satisfied

Always suggest activating the venv if it is not active.
```

**Why this structure works:**
- The YAML front matter (`---`) is required — without it, Copilot won't parse the file
- `name` is used internally for logging
- `description` is what Copilot uses to decide when to activate this skill (see [02-skill-anatomy.md](02-skill-anatomy.md))
- The body is free-form markdown — write it like instructions to a smart assistant

---

## Step 3: Commit and push

```bash
git add .github/copilot/skills/my-first-skill.md
git commit -m "feat: add my-first-skill"
git push
```

Skills are picked up automatically once the file exists in the repo — no registration step required.

---

## Step 4: Invoke the skill

In GitHub Copilot Chat (VS Code, GitHub.com, or CLI):

```
What Python version and packages are set up for this project?
```

Copilot will read the `description` of every skill in `.github/copilot/skills/`, match this query to `my-first-skill`, and respond using the instructions in the skill body.

---

## Step 5: Iterate

Skills improve through iteration. Common patterns:

| Problem | Fix |
|---------|-----|
| Copilot doesn't activate the skill | Add more trigger phrases to `description` |
| Response is too generic | Add more specific instructions to the body |
| Response ignores part of the task | Break it into numbered steps |
| Copilot activates the wrong skill | Make descriptions more distinct from each other |

Edit the file, commit, and test again. Iteration is fast.

---

## What you just learned

- Skills are markdown files with YAML front matter
- They live in `.github/copilot/skills/`
- The `description` field controls when the skill activates
- The body controls what Copilot says when the skill is active
- No CLI registration needed — commit is enough

---

→ [02-skill-anatomy.md](02-skill-anatomy.md) — every field explained in depth
