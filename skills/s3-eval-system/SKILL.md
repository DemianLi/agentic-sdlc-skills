---
name: s3-eval-system
description: >
  Use when evaluating impact scope before design — maps blast radius across
  components, schemas, APIs. Outputs impact report. NOT for solution design.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s3-eval-system`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed to `/s3-design-arch` until:
1. The impact report has been WRITTEN to `docs/arch/YYYY-MM-DD-<topic>-impact.md` and COMMITTED to git.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s3-design-arch.
Do NOT skip /s3-design-arch’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

## Workflow

### Step 1 — Load Context
Read: CONTEXT_SNAPSHOT.md (goals), CONTEXT.md (glossary), RULES.md (constraints), `docs/adr/` (ADRs).

### Step 1b — Input Sanity Check
Verify `CONTEXT_SNAPSHOT.md` before scanning: Iteration Goal is specific, REQ-N IDs present, In Scope names concrete components, Forbidden Actions exists. Any fail → stop and state what's missing.
→ Check table: `references/input-sanity-checks.md`

### Step 2 — Codebase Impact Scan
- [ ] Affected **source files** (exact paths)
- [ ] Affected **database schemas** (tables, columns, migrations)
- [ ] Affected **API endpoints** (breaking changes)
- [ ] Affected **interfaces / types** (signature changes)
- [ ] **Test files** needing updates

### Step 3 — Risk Classification
| Risk | Definition |
|---|---|
| 🔴 BREAKING | Changes existing public API contracts |
| 🟡 ADDITIVE | Adds new code without changing existing |
| 🟢 INTERNAL | Changes internal implementation only |

### Step 4 — Technical Debt Flag
Identify debt that blocks implementation: files >400 lines, missing tests, circular dependencies.

### Step 5 — Write, Commit, and Present

**Write** `docs/arch/YYYY-MM-DD-<topic>-impact.md` (template: `references/impact-report-template.md`).
**Commit**: `git add docs/arch/ && git commit -m "arch: add impact report for <topic>"`
**Present to user.** File must exist on disk; conversation summary does NOT replace it.

## Red Flags
- "可以先跳過寫文件" → 文件是 /s3-design-arch 的唯一輸入；設計會漂移
- "用戶同意了粗略版本" → 影響報告每次變更後都需重新呈現和批准
- "找不到組件就假設無影響" → 不知道 ≠ 無影響；標記 NEEDS_CONTEXT 並停下來

## Completion Report

Report status using exactly one of:
- **DONE** — `docs/arch/YYYY-MM-DD-<topic>-impact.md` written and committed; user approved; proceeding to `/s3-design-arch`.
- **DONE_WITH_CONCERNS** — file committed and approved, but note specific technical debt items that may require scope adjustment.
- **BLOCKED** — breaking change detected that conflicts with a locked ADR; state the conflict.
- **NEEDS_CONTEXT** — state exactly which parts of the codebase you cannot access or understand.

</what-to-do>

<supporting-info>

**Reads**: CONTEXT_SNAPSHOT.md, CONTEXT.md, RULES.md, docs/adr/ (optional)  
**Writes**: `docs/arch/YYYY-MM-DD-<topic>-impact.md`

## Eval Fixtures

Fixtures located at `tests/fixtures/s3-eval-system/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
