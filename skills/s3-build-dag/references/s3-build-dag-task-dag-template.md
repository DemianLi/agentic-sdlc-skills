# s3-build-dag — TASK_DAG.md Template

```markdown
# Task DAG — <Topic> — <Date>

> Execution order contract for Stage 4.
> Do NOT start a task until all dependencies are [DONE].

## Dependency Graph
<Mermaid diagram>

## Critical Path
T1 → T2 → T3 → T5 → T6 (total: 21 min)

## Parallel Opportunities
After T1: T2 and T4 can run concurrently (saves ~3 min)

## Task Execution Checklist
- [ ] TASK-1: Create DB Schema (3 min) — dependencies: none
- [ ] TASK-2: Domain Model (5 min) — dependencies: TASK-1
- [ ] TASK-3: API Handler (4 min) — dependencies: TASK-2
...
```
