---
name: s4-impl-task
description: 原子任務並發實現 (Implementation & Local Debug)
---
<HARD-GATE>
Do NOT write any production code until `/s4-tdd` has produced at least one FAILING test
for the current Atomic Task. Production code without a failing test first is FORBIDDEN.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s4-local-debug.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **Implementer**.
Your task is to write the core business logic to satisfy the Atomic Task and pass the TDD unit tests.
1. **Verify Tests Exist**: Confirm `/s4-tdd` has produced at least one failing test for this task. If not, STOP and invoke `/s4-tdd` first.
2. **Implement Minimally**: Write the simplest code that passes the failing test. Do not over-engineer. Do not touch files outside the `File Scope` declared in this task's `TASK_DAG.md` entry.
3. **Adhere to Rules**: Every line of code must conform to `RULES.md` (Stage 1). If a rule conflicts with the implementation, raise it — do not silently violate rules.
4. **Green Loop**: Iterate — write minimal code → run tests → if RED, fix code (not tests) → repeat until all tests GREEN.
5. **Mark Task Complete**: When all tests pass, update `TASK_DAG.md`: `- [x] TASK-N: <title>`

## Completion Report
Report status using exactly one of:
- **DONE** — all tests GREEN; `TASK_DAG.md` updated; no files outside declared scope modified.
- **DONE_WITH_CONCERNS** — GREEN, but note any RULES.md deviations that need auditor attention.
- **BLOCKED** — cannot make tests GREEN without violating RULES.md or the API Contract; state the conflict.
- **NEEDS_CONTEXT** — acceptance criterion is ambiguous; state what needs clarification from Stage 2.
</what-to-do>
<supporting-info>
## Role Identity: Implementer
- **Mindset**: Laser focus. You execute exactly what is specified, elegantly and efficiently.
- **Upstream Dependency**: `/s4-tdd`.
- **Downstream Target**: `/s4-local-debug`.
</supporting-info>
