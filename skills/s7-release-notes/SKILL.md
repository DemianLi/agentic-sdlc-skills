---
name: s7-release-notes
description: >
  Use when generating CHANGELOG entry from git history after deployment confirmed.
  Outputs auditable version entry. NOT for deployment decisions.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s7-release-notes`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT write to CHANGELOG.md until deploy log from `/s7-deploy` exists at
`docs/releases/YYYY-MM-DD-<version>-deploy.md` and confirms `Status: DEPLOYED` or `Status: DRY-RUN`.
Release notes describe what was shipped — writing them before deployment is a version history lie.

After updating CHANGELOG.md, proceed immediately to /s7-telemetry.
Do NOT skip /s7-telemetry's HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in the release notes phase. Task: produce auditable, version entry in CHANGELOG.md.

## Workflow

### Step 1 — Gather Source Material

| Source | Extract |
|---|---|
| git log | Commits since last tag |
| docs/specs/*.md | REQ-N titles |
| docs/audit/*.md | Breaking changes |
| docs/releases/*.md | Version, deploy mode |
| CHANGELOG.md | Previous format |

**Get commits**: `git log $(git describe --tags HEAD^ 2>/dev/null)..HEAD --oneline`

### Step 2 — Classify Changes

Map commits and REQ to category:

| Category | Contents |
|---|---|
| **Added** | New features from REQ-N / endpoints / functions |
| **Changed** | Modified behavior NOT breaking |
| **Deprecated** | Removed in future version |
| **Removed** | Removed in this version |
| **Fixed** | Bug fixes from audit/tests |
| **Security** | Security patches (SAST findings fixed) |

Only include categories with entries. Do not invent.

### Step 3 — Write CHANGELOG.md Entry

Format: Keep a Changelog + Semantic Versioning (see `references/changelog-template.md`)

Rules:
- Link to REQ-N: `(REQ-1)`
- No implementation details
- Imperative: "Add", not "Added"
- If dry-run: `> Note: validated via dry-run`

**Conditional**: If breaking changes OR API changes, add migration guide or API summary after.

### Step 4 — Prepend to CHANGELOG.md

If missing: create with header (All notable changes + format links).

If exists: prepend after `## [Unreleased]` (or header if no section).

**Commit**: `git add CHANGELOG.md && git commit -m "docs: add CHANGELOG entry for v<version>"`

---

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| Deploy not confirmed but I'll write CHANGELOG anyway | CHANGELOG is history; recording undeployed changes = lie; must wait for deploy.md Status |
| This commit is unclear, I'll guess | Guessed release notes can't be audited; if commit ≠ REQ, mark `Internal: <hash>` and skip |
| No breaking change but mention precaution anyway | Breaking = API contract change; precautions go in Changed/Fixed, not Breaking |

---

## Completion Report

- **DONE** — `CHANGELOG.md` updated with `## [vN.N.N]` block; committed. Ready for `/s7-telemetry`.
- **BLOCKED** — deploy log missing or status is `FAILED`; cannot write notes for undeployed version.
- **NEEDS_CONTEXT** — no requirements doc or git history; state what is missing.

</what-to-do>

<supporting-info>

**Reads**: git log, docs/specs/*.md, docs/audit/*.md, docs/releases/YYYY-MM-DD-<version>-deploy.md
**Writes**: CHANGELOG.md (appended)

→ Full reference: `references/detail.md`

</supporting-info>
