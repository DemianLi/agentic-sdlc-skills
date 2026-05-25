---
name: s7-release-notes
description: >
  Use when generating CHANGELOG entry from git history after deployment confirmed.
  Outputs auditable version entry. NOT for deployment decisions.
---

<HARD-GATE>

Do NOT write to CHANGELOG.md until deploy log from `/s7-deploy` exists at
`docs/releases/YYYY-MM-DD-<version>-deploy.md` and confirms `Status: DEPLOYED` or `Status: DRY-RUN`.
Release notes describe what was shipped — writing them before deployment is a version history lie.

After updating CHANGELOG.md, proceed immediately to /s7-telemetry.
Do NOT skip /s7-telemetry's HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in the release notes phase. Produce auditable version entry in CHANGELOG.md.

### Step 1 — Gather Source Material
Read: git commits since last tag (`git log $(git describe --tags HEAD^ 2>/dev/null)..HEAD --oneline`), REQ-N titles from `docs/specs/*.md`, breaking changes from `docs/audit/*.md`, version/deploy mode from `docs/releases/*.md`.

### Step 2 — Classify Changes
Map commits and REQ to categories: Added, Changed, Deprecated, Removed, Fixed, Security. Only include categories with entries. Do not invent.
→ Category definitions: `references/s7-release-notes-categories.md`

### Step 3 — Write CHANGELOG.md Entry
Format: Keep a Changelog + Semantic Versioning (→ `references/changelog-template.md`). Link REQ-N, use imperative ("Add"), no implementation details. If dry-run: add `> Note: validated via dry-run`. If breaking/API changes: append migration guide.

### Step 4 — Prepend to CHANGELOG.md
If missing: create with header. If exists: prepend after `## [Unreleased]`.
Commit: `git add CHANGELOG.md && git commit -m "docs: add CHANGELOG entry for v<version>"`

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| Deploy not confirmed but I'll write CHANGELOG anyway | CHANGELOG is history; recording undeployed changes = lie; must wait for deploy.md Status |
| This commit is unclear, I'll guess | Guessed release notes can't be audited; if commit ≠ REQ, mark `Internal: <hash>` and skip |
| No breaking change but mention precaution anyway | Breaking = API contract change; precautions go in Changed/Fixed, not Breaking |

## Completion Report

- **DONE** — `CHANGELOG.md` updated with `## [vN.N.N]` block; committed. Ready for `/s7-telemetry`.
- **BLOCKED** — deploy log missing or status is `FAILED`; cannot write notes for undeployed version.
- **NEEDS_CONTEXT** — no requirements doc or git history; state what is missing.

</what-to-do>

<supporting-info>

**Reads**: git log, docs/specs/*.md, docs/audit/*.md, docs/releases/YYYY-MM-DD-<version>-deploy.md
**Writes**: CHANGELOG.md (appended)

## Eval Fixtures

Fixtures located at `tests/fixtures/s7-release-notes/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
