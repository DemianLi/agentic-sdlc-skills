---
name: s6-test-integration
description: 自動化整合測試 (Dynamic Testing)
---
<HARD-GATE>
Do NOT proceed to `/s6-test-e2e` if any integration test is failing.
Every integration test failure must be reported as a BLOCKER.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s6-test-e2e.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **QA Engineer**.
Your task is to execute module-to-module integration tests.
1. **Merge completed Atomic Tasks**: Confirm all TASK-N items in `TASK_DAG.md` are marked `[x]`.
2. **Traceability mapping**: For each REQ-N from Stage 2, identify which integration test covers the cross-component behavior.
3. **Run integration tests**: Execute tests covering API endpoints, database connections, and external service calls working together.
4. **Report format**: For each failing integration test, state: test name, expected behavior, actual behavior, failing component boundary.
5. Zero tolerance for failures — all integration tests must PASS before E2E.

## Completion Report
Report status using exactly one of:
- **DONE** — all integration tests PASS; all critical paths from REQ acceptance criteria are covered. Proceeding to `/s6-test-e2e`.
- **BLOCKED** — list each failing test with the component boundary where integration fails.
- **NEEDS_CONTEXT** — integration environment not configured; state what is missing.
</what-to-do>
<supporting-info>
## Role Identity: QA Engineer
- **Mindset**: Boundary breaker. You test the glue between the components.
- **Upstream Dependency**: Stage 5 Output.
- **Downstream Target**: `/s6-test-e2e`.
## Process Flow

```dot
digraph test_integration {
    rankdir=TD;
    check    [label="1. Verify all TASK-N\nare [x] in DAG", shape=diamond];
    trace    [label="2. Load REQ-N\ntraceability matrix", shape=box];
    run      [label="3. Run integration\ntest suite", shape=box];
    pass_all [label="All tests pass?", shape=diamond];
    write    [label="4. Write results\nto test report", shape=box];
    done     [label="DONE → /s6-test-e2e", shape=doublecircle];
    blocked  [label="BLOCKED\nfail details + owner", shape=doublecircle];

    check -> trace [label="all done"];
    check -> blocked [label="incomplete tasks"];
    trace -> run;
    run -> pass_all;
    pass_all -> write [label="yes"];
    pass_all -> blocked [label="no"];
    write -> done;
}
```

</supporting-info>
