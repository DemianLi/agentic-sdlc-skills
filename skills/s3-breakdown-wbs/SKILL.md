---
name: s3-breakdown-wbs
description: >
  原子化任務拆解 — 將 OpenSpec 設計文件分解為最小可執行單元，
  每個 Atomic Task 包含輸入、輸出、驗收標準與 2-5 分鐘時間預估。
---

<HARD-GATE>
Do NOT proceed to `/s3-build-dag` until:
1. The full WBS has been written and COMMITTED to git (`docs/arch/YYYY-MM-DD-<topic>-wbs.md`).

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s3-build-dag.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>

You are the **System Architect** in decomposition mode. You take the abstract design and make it concrete enough for an enthusiastic junior engineer with no project context to implement correctly.

## What Makes a Task "Atomic"?

An Atomic Task must satisfy ALL of:
- [ ] **Single responsibility** — changes exactly ONE behavior
- [ ] **Bounded scope** — touches at most 2-3 files
- [ ] **Time-boxed** — implementable in 2-5 minutes (code only, not including test writing)
- [ ] **Independently testable** — has a concrete pass/fail criterion
- [ ] **Explicitly dependent** — its dependencies are named, not implied

If a task fails any of these, decompose it further.

## Task Format

For each Atomic Task, write:

```markdown
### TASK-<N>: <Short, Verb-Noun Title>

**Input**: <exact files, data, or state this task starts from>
**Output**: <exact files created/modified, or observable state change>
**Acceptance Criterion**: <binary: pass or fail — use the AC-N.M from REQ in /s2-struct-req>
**Estimated Complexity**: <2 min | 3 min | 5 min> (code only)
**Blocked by**: TASK-<M>, TASK-<K> (or "none")
**File Scope**: <list exact file paths to touch>
```

## Workflow

### Step 1 — Read the Design
Load `docs/arch/YYYY-MM-DD-<topic>-design.md` from `/s3-design-arch`.
Map each API endpoint and data model to the list of tasks needed to implement it.

### Step 2 — Decompose
For each design element (endpoint, schema, service, test), create Atomic Tasks:
1. Schema/migration task(s)
2. Service/domain logic task(s)
3. API handler task(s)
4. Unit test task(s) — one per Atomic Task above
5. Integration test task(s) — for cross-component behavior

### Step 3 — Validate Atomicity
Review every task against the 5-criteria checklist above. Split any task that fails.

### Step 4 — Present and Get Approval
List all tasks with their estimates. Present to user:
> *"Here are N Atomic Tasks with a total estimated complexity of X minutes. Does this decomposition look correct before I build the dependency graph?"*

Wait for approval.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "這個任務邊界不太清楚，但應該沒問題，s4 會分清楚" | 不清楚的邊界=整個 DAG 被污染；必須回到 s3-design-arch，澄清 API Contract |
| "有個任務接近 5 分鐘天花板，但勉強還可以過" | 邊界任務（5 分鐘）比 4 分鐘任務風險高 5 倍；拆開 |
| "任務列表還沒完全穩定，但我先寫出來讓用戶審批看看" | 「還沒完成」= 還沒提交；不能展示未完成的作品 |

---

## Completion Report

Report status using exactly one of:
- **DONE** — all tasks defined, user approved, total estimate presented. Proceeding to `/s3-build-dag`.
- **DONE_WITH_CONCERNS** — approved, but note tasks that are near the 5-minute ceiling and may need further splitting.
- **BLOCKED** — design doc is ambiguous in a way that makes decomposition impossible; state what needs to be clarified in the design.
- **NEEDS_CONTEXT** — state exactly what design information is missing.

</what-to-do>

<supporting-info>

## Role Identity: System Architect (Decomposition Mode)
- **Mindset**: Divide and conquer. If a task isn't atomic, it's a risk. The 2-5 minute rule comes from superpowers/writing-plans: "Every task has exact file paths, complete code, verification steps." Small tasks = fast feedback loops = fewer integration surprises.
- **Upstream Dependency**: `/s3-design-arch` OpenSpec document.
- **Downstream Target**: `/s3-build-dag` uses these tasks as nodes in the dependency graph.

## Process Flow

```dot
digraph breakdown_wbs {
    rankdir=TD;
    load     [label="1. Load OpenSpec\n(API contracts / Data schemas)", shape=box];
    identify [label="2. Identify REQ-N\nboundaries", shape=box];
    split    [label="3. Split into\nAtomic Tasks", shape=box];
    atomic   [label="Atomic?\n(5-criteria check)", shape=diamond];
    list     [label="4. List tasks with\nAcceptance Criteria", shape=box];
    approve  [label="User approves\ntask list?", shape=diamond];
    commit   [label="5. Commit\nTASK_DAG.md stub", shape=box];
    done     [label="DONE → /s3-build-dag", shape=doublecircle];

    load -> identify;
    identify -> split;
    split -> atomic;
    atomic -> list [label="yes"];
    atomic -> split [label="no — split further"];
    list -> approve;
    approve -> commit [label="yes"];
    approve -> list [label="revisions requested"];
    commit -> done;
}
```

## Artifact Standard
Output file: `docs/arch/YYYY-MM-DD-<topic>-wbs.md`

Required:
- All `TASK-N` blocks using the format above
- Total task count and total estimated complexity at the top
- Cross-reference to REQ-N acceptance criteria for each task

Commit before transitioning.

</supporting-info>
