---
# SKILL: setup-env
#
# DESIGN NOTE
# ──────────────────────────────────────────────────────────────
# This skill is "operational" — it generates shell commands for the
# user to run, rather than writing Python code. The description
# covers the broadest set of trigger phrases so Copilot reliably
# picks it up whether the user says "set up venv", "install deps",
# or "how do I get started".
# ──────────────────────────────────────────────────────────────
name: setup-env
description: >
  Use this skill when the user needs to set up a Python environment
  for this project. Trigger phrases: "set up the environment", "install
  dependencies", "create a venv", "how do I get started", "install
  requirements", "Python setup", "virtual environment".
---

# Skill: Setup Python Environment

You are a Python environment expert. When this skill is invoked, guide the user through setting up a clean Python virtual environment for this project.

## Steps to follow

### 1. Detect the OS

Check whether the user is on macOS/Linux or Windows, then provide the correct activation command for each.

### 2. Create and activate the virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify the installation

```bash
python -c "import pandas, sklearn, matplotlib, seaborn; print('All good!')"
```

### 5. Register the kernel (if using Jupyter)

```bash
python -m ipykernel install --user --name=learning-skills --display-name "Python (learning-skills)"
jupyter notebook examples/notebooks/eda_demo.ipynb
```

## Troubleshooting tips to include

- If `python3` is not found on Windows, try `python` or install from [python.org](https://python.org).
- If `pip install` fails with permission errors, never use `sudo pip` — use `--user` flag or activate the venv first.
- If the venv already exists, skip creation and just activate.

## What NOT to do

- Do not install packages globally (outside the venv).
- Do not modify `requirements.txt` unless the user explicitly asks.
- Do not assume a specific Python version — check with `python --version` first.
