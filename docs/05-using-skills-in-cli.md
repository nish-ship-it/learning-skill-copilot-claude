# 05 — Using Skills in the Copilot CLI

> This doc explains the mechanics of how skills are invoked in the Copilot CLI — including a critical distinction that trips up almost everyone new to this tool.

---

## Two tools, one name — know which one you're using

When people say "GitHub Copilot CLI", they usually mean one of two separate tools:

| Tool | Command | Purpose | Has skills? |
|------|---------|---------|-------------|
| **`gh copilot`** | `gh copilot suggest`, `gh copilot explain` | Translates natural language into shell commands | ❌ No skill system |
| **`copilot`** (Copilot CLI agent) | `copilot` | Full agentic coding assistant in your terminal | ✅ Yes — reads `.github/copilot/skills/` |

**The skills we build in this repo only work with the `copilot` agent, not `gh copilot suggest`.**

Install the `copilot` agent:
```bash
curl -fsSL https://gh.io/copilot-install | bash
# or
brew install copilot-cli
# or
npm install -g @github/copilot
```

---

## How to add skills to a project

Skills live in `.github/copilot/skills/` as markdown files:

```
your-project/
└── .github/
    └── copilot/
        └── skills/
            ├── explore-dataset.md    ← one skill per file
            ├── setup-env.md
            └── explain-notebook.md
```

**No registration required.** The `copilot` agent discovers every `.md` file in this directory automatically when launched in the project.

Each skill file must have YAML front matter with `name:` and `description:`:

```markdown
---
name: explore-dataset
description: >
  Use this skill when the user wants to explore, analyse, or profile a
  CSV or DataFrame. Trigger phrases: "explore the data", "EDA", "check for nulls".
---

# Your instructions here...
```

See [02-skill-anatomy.md](02-skill-anatomy.md) for a full breakdown of every field.

---

## How to manage skills in an active session

Once `copilot` is running in your project, use these slash commands:

```
/skills                  → list all skills Copilot has loaded for this project
/instructions            → view which instruction files are active
```

The `/skills` output will show your project skills (from `.github/copilot/skills/`) and any personal skills you've added.

---

## How to invoke a skill

You don't call skills directly — you just **ask in natural language**. Copilot reads the `description:` field of every skill and activates the best match.

**Example session:**

```
$ copilot
# (Copilot starts, reads .github/copilot/skills/)

You: explore examples/data/sample.csv, target column is income_bracket

# Copilot matches your prompt to the explore-dataset skill's description,
# then follows the skill's instructions to run a full EDA.
```

```
You: set up the Python environment for this project

# Matches setup-env skill → walks you through venv creation + pip install
```

```
You: explain what examples/notebooks/eda_demo.ipynb does

# Matches explain-notebook skill → structured notebook breakdown
```

---

## Where the `copilot` agent reads instructions from

The agent automatically loads context from these locations (in addition to skills):

| File | Scope |
|------|-------|
| `.github/copilot-instructions.md` | Project — applies to everyone who clones the repo |
| `AGENTS.md` | Project |
| `CLAUDE.md` | Project |
| `~/.copilot/copilot-instructions.md` | Personal — applies across all your repos |
| `.github/instructions/**/*.instructions.md` | Project |

This means your `copilot-instructions.md` (which we have in this repo) gives every session context about the project's architecture and conventions — automatically, before any skill activates.

---

## Skill activation tips

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Copilot doesn't seem to use my skill | `description:` is too vague | Add explicit trigger phrases your teammates actually say |
| Wrong skill activates | Two skills have overlapping descriptions | Make descriptions more distinct; prefix with the specific context |
| Skill activates but ignores part of the instruction | Body is too long | Break one big skill into two focused ones |
| `/skills` shows no project skills | Wrong directory path | Path must be exactly `.github/copilot/skills/` |

---

## Personal skills (cross-repo)

If you have skills that should apply across *all* your projects (not just this repo), put them in:

```
~/.copilot/skills/
└── my-personal-skill.md
```

Same format, same rules — just a different location. Useful for personal preferences, your go-to debugging steps, or company-wide standards before they're added to individual repos.

---

→ Back to [README](../README.md)
