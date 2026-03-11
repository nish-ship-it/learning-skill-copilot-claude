# 00 — What are GitHub Copilot CLI Skills?

## The mental model

Think of a **skill** as a specialist you can hire for a specific task.

Without skills, Copilot knows a lot but has no context about *your* project. Skills give Copilot focused, opinionated knowledge about a particular task in your specific codebase.

```
Without skill:  You → Copilot (generic assistant)
With skill:     You → Copilot + explore-dataset skill (expert EDA analyst who knows your repo)
```

---

## Two kinds of help Copilot CLI gives you

| Mode | What it does | Example |
|------|-------------|---------|
| `gh copilot suggest` | Translates a task description into a shell command | "list all CSV files modified today" → `find . -name "*.csv" -mtime -1` |
| `gh copilot explain` | Explains what a shell command does | `awk '{sum+=$2} END{print sum}'` → plain English breakdown |

Skills extend the **suggest** mode — they give Copilot a richer instruction set so it produces better, project-aware suggestions.

---

## Where skills live

```
your-repo/
└── .github/
    └── copilot/
        └── skills/
            └── your-skill-name.md    ← one file per skill
```

Copilot reads every `.md` file in this folder when it is active in your project. This means:
- Skills are **version-controlled** — tracked in git like any other file
- Skills are **automatically shared** with everyone who clones the repo
- Skills are **scoped to the project** — they don't affect other repos

---

## How Copilot picks the right skill

Each skill file has a `description` in its YAML front matter. Copilot reads *all* descriptions and uses them to decide which skill is most relevant to the user's query.

This is why the description field matters so much — it's effectively the skill's "activation phrase". See [02-skill-anatomy.md](02-skill-anatomy.md) for how to write good descriptions.

---

## What skills are NOT

- Skills are not code that runs automatically — they are instruction sets that guide Copilot's responses
- Skills are not the same as GitHub Actions workflows
- Skills cannot access external APIs or the internet on their own

---

## Next step

→ [01-creating-first-skill.md](01-creating-first-skill.md) — build and invoke your first skill in under 10 minutes
