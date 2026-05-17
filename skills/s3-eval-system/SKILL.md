---
name: s3-eval-system
description: >
  Use before designing any change that touches existing code — maps blast radius
  across components, DB schemas, and APIs before anyone writes a line.
---

<HARD-GATE>
Do NOT proceed to `/s3-design-arch` until:
1. The impact report has been WRITTEN to `docs/arch/YYYY-MM-DD-<topic>-impact.md` and COMMITTED to git.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s3-design-arch.
Do NOT skip /s3-design-arch’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **System Architect** in evaluation mode. Your job is risk identification, not solution design. Find the blast radius before anyone touches code.

## Workflow

### Step 1 — Load Context
Read in this order:
1. `CONTEXT_SNAPSHOT.md` — iteration goals and scope
2. `CONTEXT.md` — domain glossary (use exact terms when naming components)
3. `RULES.md` — architectural constraints
4. `docs/adr/` — existing architectural decisions

### Step 1b — Input Sanity Check

After loading `CONTEXT_SNAPSHOT.md`, verify the following before scanning the codebase. If any check fails, **stop and state exactly what is missing. Do not begin the impact scan.**

| Check | What to verify | If it fails |
|---|---|---|
| `## Iteration Goal` is specific | One concrete goal — not a vague phrase like "improve the feature" or "refactor the module" | Ask: "What specific behavior should change? Please rewrite the goal as one sentence with a subject and verb." |
| `## Must-Have Requirements` lists REQ-N IDs | At least one `REQ-1`, `REQ-2`, etc. referencing an actual requirements doc | Ask: "Which requirements from Stage 2 are in scope? Please list REQ-N IDs from the requirements doc." |
| `## In Scope` names concrete components | Lists specific files, routes, or user flows — not just "the checkout module" | Ask: "Which specific files, routes, or components are in scope? The impact scan cannot proceed without a concrete boundary." |
| `## Forbidden Actions` exists | Explicit list of what must NOT be changed this iteration | Ask: "What should I absolutely not touch during this iteration? This section is required." |

### Step 2 — Codebase Impact Scan
For each in-scope requirement from the snapshot:
- [ ] Identify affected **source files** (list exact paths)
- [ ] Identify affected **database schemas** (tables, columns, migrations needed)
- [ ] Identify affected **API endpoints** (breaking changes to request/response contracts)
- [ ] Identify affected **interfaces / types** (type signature changes)
- [ ] Identify **test files** that need updating

### Step 3 — Risk Classification
Classify each change by blast radius:

| Risk Level | Definition | Example |
|---|---|---|
| 🔴 BREAKING | Changes existing public API contracts | Renaming a field, changing response type |
| 🟡 ADDITIVE | Adds new code without changing existing | New endpoint, new table column |
| 🟢 INTERNAL | Changes internal implementation only | Refactoring a private function |

### Step 4 — Technical Debt Flag
Note any existing technical debt in the affected areas that might impede implementation:
- Files over 400 lines (violates RULES.md)
- Missing tests on affected paths (blocks TDD in Stage 4)
- Circular dependencies near the change boundary

### Step 5 — Write, Commit, and Present Impact Report

**Step 5a — Write to disk (REQUIRED before presenting)**

Determine today's date and write the report to:
`docs/arch/YYYY-MM-DD-<topic>-impact.md`

Required content:
```
## Impact Report — <Iteration Topic>

### Breaking Changes (🔴)
- <component>: <what changes> → <migration needed>

### Additive Changes (🟡)
- <component>: <what is added>

### Technical Debt to Resolve First
- <file/area>: <debt description> — must fix before Stage 4 can proceed

### Recommended Approach
<1-2 sentences on recommended strategy for /s3-design-arch>
```

**Step 5b — Commit**

```bash
git add docs/arch/
git commit -m "arch: add impact report for <topic>"
```

**Step 5c — Present and wait**

Show the user the file path and full content. **Wait for explicit approval before proceeding.**
A conversation summary does NOT replace the file. If the file does not exist on disk, this step is not done.

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

## Role Identity: System Architect (Evaluation Mode)
- **Mindset**: Risk mitigation. You look for the blast radius of new changes. Your job is to surface surprises NOW, not after Stage 4 has written 2,000 lines of code.
- **Upstream Dependency**: `CONTEXT_SNAPSHOT.md` from Stage 2.
- **Downstream Target**: `/s3-design-arch` uses your impact report as the primary input for design decisions.

## Process Flow

```dot
digraph eval_system {
    rankdir=TD;
    load     [label="1. Load Context\n(CONTEXT_SNAPSHOT / CONTEXT.md /\nRULES.md / ADRs)", shape=box];
    scan     [label="2. Codebase Impact Scan\n(files / schemas / endpoints / types / tests)", shape=box];
    classify [label="3. Risk Classification\n🔴 BREAKING / 🟡 ADDITIVE / 🟢 INTERNAL", shape=box];
    debt     [label="4. Technical Debt Flag\n(>400 lines / missing tests / circular deps)", shape=box];
    debt_ok  [label="Blocking debt\nfound?", shape=diamond];
    report   [label="5. Present Impact Report\nto user", shape=box, style=filled, fillcolor="#cce0ff"];
    approve  [label="User approves?", shape=diamond];
    done     [label="DONE\nProceed to /s3-design-arch", shape=doublecircle];
    blocked  [label="BLOCKED\nADR conflict or\nunresolvable debt", shape=doublecircle];

    load -> scan;
    scan -> classify;
    classify -> debt;
    debt -> debt_ok;
    debt_ok -> report [label="no blocking debt"];
    debt_ok -> blocked [label="yes — conflicts with ADR"];
    report -> approve;
    approve -> done [label="approved"];
    approve -> blocked [label="major concern unresolved"];
}
```

## Artifact Standard
Output file: `docs/arch/YYYY-MM-DD-<topic>-impact.md`

Required sections: Breaking Changes / Additive Changes / Technical Debt / Recommended Approach

Commit before transitioning.

## Artifact Dependencies
- **Reads**: `CONTEXT_SNAPSHOT.md`, `CONTEXT.md`, `RULES.md`, `docs/adr/` (optional)
- **Writes**: `docs/arch/YYYY-MM-DD-<topic>-impact.md`

</supporting-info>
