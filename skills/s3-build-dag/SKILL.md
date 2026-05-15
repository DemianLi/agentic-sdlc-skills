---
name: s3-build-dag
description: >
  依賴拓撲建立 — 將 Atomic Tasks 組織為可機器解析的 DAG，
  使用 Mermaid 語法輸出，標注並行機會與關鍵路徑，產出 TASK_DAG.md。
---

<HARD-GATE>
Do NOT output TASK_DAG.md until you have verified that:
1. The graph has NO cycles (it must be a true Directed Acyclic Graph).
2. Every task from the WBS appears as exactly one node.
3. The user has approved the dependency graph before Stage 4 begins.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s4-impl-task (Stage 4 Implementer).”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>

You are the **System Architect** in orchestration mode. You transform the flat task list into an executable ordering that maximizes parallelism while respecting hard dependencies.

## Workflow

### Step 1 — Load Tasks
Read `docs/arch/YYYY-MM-DD-<topic>-wbs.md` from `/s3-breakdown-wbs`.
List all TASK-N items and their `Blocked by` declarations.

### Step 2 — Build the Dependency Graph
For each task, draw edges from its dependencies to itself:
- `TASK-A → TASK-B` means B cannot start until A is complete
- Tasks with no dependencies can start immediately (parallel entry points)

### Step 3 — Output: Mermaid DAG

```mermaid
graph TD
    T1["TASK-1: Create DB Schema\n⏱ 3 min"]
    T2["TASK-2: Domain Model\n⏱ 5 min"]
    T3["TASK-3: API Handler\n⏱ 4 min"]
    T4["TASK-4: Unit Tests — Schema\n⏱ 3 min"]
    T5["TASK-5: Unit Tests — Handler\n⏱ 4 min"]
    T6["TASK-6: Integration Test\n⏱ 5 min"]

    T1 --> T2
    T1 --> T4
    T2 --> T3
    T3 --> T5
    T4 --> T6
    T5 --> T6
```

Label each node with: task name + estimated complexity.

### Step 4 — Identify Key Path and Parallel Tracks

After building the graph, annotate:

```markdown
## Critical Path
T1 → T2 → T3 → T5 → T6 (total: 21 min)

## Parallel Opportunities
After T1 completes: T2 and T4 can run concurrently (saves ~3 min)
```

### Step 5 — Output TASK_DAG.md

Write `TASK_DAG.md` at the project root:

```markdown
# Task DAG — <Topic> — <Date>

> This file is the execution order contract for Stage 4.
> Do NOT start a task until all its dependencies are marked [DONE].

## Dependency Graph
<Mermaid diagram here>

## Critical Path
<list>

## Parallel Opportunities
<list>

## Task Execution Checklist
- [ ] TASK-1: Create DB Schema (3 min) — dependencies: none
- [ ] TASK-2: Domain Model (5 min) — dependencies: TASK-1
- [ ] TASK-3: API Handler (4 min) — dependencies: TASK-2
...
```

Present to user and wait for approval before committing.

---

## Completion Report

Report status using exactly one of:
- **DONE** — `TASK_DAG.md` committed, user approved. Stage 4 can begin with TASK-1.
- **DONE_WITH_CONCERNS** — committed, but note any tasks with high complexity or unclear dependencies.
- **BLOCKED** — detected a cycle in the dependency graph; state which tasks form the cycle.
- **NEEDS_CONTEXT** — state exactly what task dependency information is unclear.

</what-to-do>

<supporting-info>

## Role Identity: System Architect (Orchestration Mode)
- **Mindset**: Optimize for concurrent delivery while respecting hard dependencies. Every hour saved in Stage 4 through smart parallelism is an hour of engineering time returned to the user.
- **Upstream Dependency**: `/s3-breakdown-wbs` — the full task list with dependencies.
- **Downstream Target**: Stage 4 Implementer reads `TASK_DAG.md` as their first action. The checklist `[ ]` boxes are the Agent's progress tracker.

## Process Flow

```dot
digraph build_dag {
    rankdir=TD;
    load     [label="1. Load Atomic Tasks\n(TASK_DAG.md stub)", shape=box];
    deps     [label="2. Identify Dependencies\nfor each task", shape=box];
    graph    [label="3. Build DAG\n(topological order)", shape=box];
    cycle    [label="Cycle detected?", shape=diamond];
    path     [label="4. Compute Critical Path\n& parallel groups", shape=box];
    approve  [label="User approves\nDAG?", shape=diamond];
    commit   [label="5. Commit\nfinal TASK_DAG.md", shape=box];
    done     [label="DONE → Stage 4", shape=doublecircle];
    blocked  [label="BLOCKED\nresolve cycle", shape=doublecircle];

    load -> deps;
    deps -> graph;
    graph -> cycle;
    cycle -> blocked [label="yes"];
    cycle -> path [label="no"];
    path -> approve;
    approve -> commit [label="yes"];
    approve -> deps [label="revisions"];
    commit -> done;
}
```

## Artifact Standard
Output file: `TASK_DAG.md` at project root (not in `docs/` — it is the active execution guide)

Required sections:
- Mermaid graph with time annotations on each node
- Critical Path calculation
- Parallel Opportunities list
- Execution Checklist with `[ ]` boxes

Commit before transitioning.

</supporting-info>
