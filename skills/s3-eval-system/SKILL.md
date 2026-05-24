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

After loading `CONTEXT_SNAPSHOT.md`, verify the following before scanning the codebase. If any check fails, **stop and state exactly what is missing. Do not begin the impact scan.**

| Check | What to verify | If it fails |
|---|---|---|
| `## Iteration Goal` is specific | One concrete goal — not a vague phrase like "improve the feature" or "refactor the module" | Ask: "What specific behavior should change? Please rewrite the goal as one sentence with a subject and verb." |
| `## Must-Have Requirements` lists REQ-N IDs | At least one `REQ-1`, `REQ-2`, etc. referencing an actual requirements doc | Ask: "Which requirements from Stage 2 are in scope? Please list REQ-N IDs from the requirements doc." |
| `## In Scope` names concrete components | Lists specific files, routes, or user flows — not just "the checkout module" | Ask: "Which specific files, routes, or components are in scope? The impact scan cannot proceed without a concrete boundary." |
| `## Forbidden Actions` exists | Explicit list of what must NOT be changed this iteration | Ask: "What should I absolutely not touch during this iteration? This section is required." |

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

**Write to disk (REQUIRED):** `docs/arch/YYYY-MM-DD-<topic>-impact.md`

```
## Impact Report — <Iteration Topic>
### Breaking Changes (🔴)
- <component>: <what changes> → <migration needed>
### Additive Changes (🟡)
- <component>: <what is added>
### Technical Debt to Resolve First
- <file/area>: <debt description>
### Recommended Approach
<1-2 sentences>
```

**Commit:** `git add docs/arch/ && git commit -m "arch: add impact report for <topic>"`

**Present to user and proceed to /s3-design-arch.** File must exist on disk; conversation summary does NOT replace it.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "影響分析看起來差不多，可以先跳過寫文件" | 文件是後續 s3-design-arch 的唯一輸入；沒有承諾的文字，設計會漂移 |
| "用戶同意了之前的粗略版本，不需要再問一次" | 影響報告提交後的每一次變更都需要重新呈現和批准 |
| "找不到某些組件，就假設沒有受到影響" | 不知道 ≠ 無影響；「無法存取」要停下來、列出具體障礙，並在報告中標記 NEEDS_CONTEXT |

---

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

→ Full reference: `references/detail.md`

</supporting-info>
