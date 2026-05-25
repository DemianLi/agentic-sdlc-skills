---
name: s3-breakdown-wbs
description: >
  Use when decomposing design into atomic tasks — explicit scope, inputs, outputs,
  acceptance criteria. Outputs WBS file. NOT for design creation.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s3-breakdown-wbs`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed to `/s3-build-dag` until:
1. The full WBS has been written and COMMITTED to git (`docs/arch/YYYY-MM-DD-<topic>-wbs.md`).

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s3-build-dag.
Do NOT skip /s3-build-dag’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **System Architect** in decomposition mode. Make design concrete enough for a junior engineer to implement correctly.

**Atomic Task requirements**: single responsibility, ≤2-3 files, implementable in 2-5 min, independently testable, explicitly dependent. Any failure → decompose further.
→ Task format template: `references/s3-breakdown-wbs-task-format.md`

### Step 1 — Load Design
Read `docs/arch/YYYY-MM-DD-<topic>-design.md`. Map each endpoint/schema to tasks needed.

### Step 2 — Decompose Into Tasks
For each design element: Schema/migration task(s), Service/domain logic task(s), API handler task(s), Unit test task(s), Integration test task(s).

### Step 3 — Validate Atomicity
Review all tasks against 5-criteria checklist (single responsibility, bounded scope, time-boxed, independently testable, explicitly dependent). Split any failures.

### Step 4 — Present for Approval
List all tasks + total estimated complexity. Get user sign-off before building DAG.

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "這個任務邊界不太清楚，但應該沒問題，s4 會分清楚" | 不清楚的邊界=整個 DAG 被污染；必須回到 s3-design-arch，澄清 API Contract |
| "有個任務接近 5 分鐘天花板，但勉強還可以過" | 邊界任務（5 分鐘）比 4 分鐘任務風險高 5 倍；拆開 |
| "任務列表還沒完全穩定，但我先寫出來讓用戶審批看看" | 「還沒完成」= 還沒提交；不能展示未完成的作品 |

## Completion Report

- **DONE** — all tasks defined, user approved, total estimate presented. Proceeding to `/s3-build-dag`.
- **DONE_WITH_CONCERNS** — approved, but note tasks that are near the 5-minute ceiling and may need further splitting.
- **BLOCKED** — design doc is ambiguous in a way that makes decomposition impossible; state what needs to be clarified in the design.
- **NEEDS_CONTEXT** — state exactly what design information is missing.

</what-to-do>

<supporting-info>

**Reads**: `docs/arch/YYYY-MM-DD-<topic>-design.md`  
**Writes**: `docs/arch/YYYY-MM-DD-<topic>-wbs.md`

→ Full reference: `references/detail.md`

</supporting-info>
