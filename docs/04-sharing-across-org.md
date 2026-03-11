# 04 — Sharing Skills Across Your Org

There are three levels of sharing: **within a project**, **across projects in your org**, and **with the public**. Each has a different mechanism.

---

## Level 1: Within a project (automatic)

If your skills are in `.github/copilot/skills/`, every collaborator who opens the repo with Copilot gets them automatically. Nothing to do.

**Checklist:**
- [ ] Skills are committed (not in `.gitignore`)
- [ ] The `.github/copilot/skills/` path is exact

---

## Level 2: Across multiple repos in your org

### Option A — Shared skills repo (recommended)

Create a dedicated repo (e.g., `your-org/copilot-skills`) that only contains skills:

```
your-org/copilot-skills/
├── .github/copilot/skills/
│   ├── explore-dataset.md
│   ├── setup-env.md
│   └── explain-notebook.md
└── README.md    ← explains how to adopt these skills
```

Teams adopt shared skills by **copying** the skill files they need into their own repo. This is intentional — it gives each team the ability to customise without affecting others.

**Workflow:**
```bash
# In your project repo
cp -r ../copilot-skills/.github/copilot/skills/ .github/copilot/skills/

# Customise as needed, then commit
git add .github/copilot/skills/
git commit -m "feat: adopt org copilot skills"
```

### Option B — Git submodule

For teams that want updates to flow automatically:

```bash
# In your project repo
git submodule add https://github.com/your-org/copilot-skills .copilot-shared
# Then symlink or copy skills as needed
```

Submodules add complexity — only use them if the team is comfortable with git submodule workflows.

### Option C — Org-level copilot-instructions.md

Add shared context (not full skills) to your org's `.github` repo:

```
your-org/.github/
└── copilot-instructions.md    ← applies to all repos in the org automatically
```

This is for **context** (coding standards, team conventions), not for full skill definitions.

---

## Level 3: Public sharing (this repo's approach)

This repo is public with an MIT license. Anyone can:

1. **Fork** the repo and adapt the skills for their stack
2. **Copy individual skill files** into their own project
3. **Reference the docs** in their own onboarding materials

### Recommended approach for your org

1. Fork this repo as `your-org/copilot-skills-ml`
2. Replace `examples/` with your real data and notebooks
3. Update the skills to match your team's actual conventions
4. Keep the docs — they teach the skill-writing pattern, not just the examples
5. Share the repo link in your team's onboarding checklist

---

## How to document skills for your team

A good skill README covers:
1. **What the skill does** (one sentence)
2. **When to use it** (trigger phrases, use cases)
3. **How to invoke it** (example Copilot prompt)
4. **How to customise it** (what parts are team-specific)

The skill files in this repo follow this pattern — the comments inside the YAML front matter are the "why", and the body is the "what".

---

## Keeping skills up to date

Skills go stale when:
- Your codebase changes (new libraries, new conventions)
- The team learns better patterns
- Copilot's capabilities evolve

**Recommended cadence:**
- Review skills quarterly or after major project changes
- Treat skill updates like any other code change — PR + review
- Keep a `CHANGELOG` section at the top of long-lived skills

---

## Governance for larger orgs

| Concern | Approach |
|---------|----------|
| Who can add skills? | Require PR review from a data/ML lead |
| How to test a skill? | Test against a known prompt before merging |
| How to retire a skill? | Move to `skills/archive/` rather than deleting — preserves history |
| Naming collisions across teams | Prefix with team name: `ds-explore-dataset.md` |

---

## Summary: sharing path

```
You write a skill → commit to project repo          (Level 1: your project)
      ↓
Copy to org skills repo + PR                         (Level 2: your org)
      ↓
Make repo public + MIT license + good README         (Level 3: community)
```

This repo sits at Level 3. Start at Level 1 and work your way up as your skills mature.
