---
name: s3-build-dag
description: >
  Use when establishing task execution order and parallelism from WBS tasks. Outputs
  TASK_DAG.md with dependency graph and critical path. NOT for task decomposition.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s3-build-dag`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed to Stage 4 until TASK_DAG.md has been written and COMMITTED to git.

After presenting the required artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed to /s4-impl-task (Stage 4 Implementer)."
</HARD-GATE>

<what-to-do>

You are the **System Architect** in orchestration mode. Transform the flat task list into an executable ordering that maximizes parallelism while respecting hard dependencies.

### Step 1 — Load Tasks
Read `docs/arch/YYYY-MM-DD-<topic>-wbs.md`. List all TASK-N items and `Blocked by` declarations.

### Step 2 — Build Dependency Graph
For each task, draw edges: `TASK-A → TASK-B` = B blocked until A done. No dependencies = parallel entry points.

### Step 3 — Output Mermaid DAG
Build graph with nodes labeled: task name + time estimate. Example: `TASK-1: DB Schema (3 min)` → `TASK-2: Domain Model (5 min)`.

### Step 4 — Critical Path & Parallel Tracks
Annotate: Critical Path (T1 → T2 → total min) and Parallel Opportunities (which tasks can run concurrently).

### Step 5 — Write TASK_DAG.md
Write `TASK_DAG.md` at project root with Mermaid diagram, Critical Path, Parallel Opportunities, and Task Execution Checklist.
→ TASK_DAG.md template: `references/s3-build-dag-task-dag-template.md`
Present to user and wait for approval before committing.

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| "Graph looks complex, might have cycle, show user anyway" | Any cycle suspicion = real signal; topo sort failure = DAG invalid; fix WBS first |
| "Task dependency is fuzzy, assume current order is OK" | Fuzzy dependency = uncertain execution order; risk deadlock; back to WBS, clarify AC boundaries |
| "Critical path is longer than expected but optimal" | Long path = insufficient WBS decomposition; Stage 4 will block; decompose now |

## Completion Report

- **DONE** — `TASK_DAG.md` committed, user approved. Stage 4 begins with TASK-1.
- **DONE_WITH_CONCERNS** — committed, but note tasks with high complexity or unclear dependencies.
- **BLOCKED** — cycle detected in dependency graph; state which tasks form the cycle.
- **NEEDS_CONTEXT** — state exactly what task dependency info is unclear.

</what-to-do>

<supporting-info>

**Reads**: docs/arch/YYYY-MM-DD-<topic>-wbs.md
**Writes**: TASK_DAG.md

→ Full reference: `references/detail.md`

</supporting-info>
