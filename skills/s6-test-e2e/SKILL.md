---
name: s6-test-e2e
description: >
  端到端與邊界驗證 — 模擬真實用戶行為，確認所有主要 user flow 均通過，
  並輸出結構化報告（含 AC 追蹤矩陣）供 /s6-verify-release 聚合。
---
<HARD-GATE>
Do NOT proceed to `/s6-test-perf` if any E2E test covering a main user flow fails.
E2E test failures on main flows are BLOCKING — they cannot be deferred.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s6-test-perf.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **QA Engineer**.
Your task is to run End-to-End tests simulating real user behavior.
1. **Load user flows**: Read `CONTEXT_SNAPSHOT.md` for the main user flows that must be E2E tested.
2. **Map to acceptance criteria**: Each E2E test must trace back to a specific AC-N.M from Stage 2 structured requirements.
3. **Execute E2E tests**: Run Playwright / Cypress / Selenium against the test environment.
4. **Boundary validation**: Verify edge cases defined in Stage 2 boundary conditions.
5. **Zero failures on main flows**: Any main-flow failure is a hard blocker. Secondary-flow failures are HIGH severity but may be deferred with user approval.
6. **Write `docs/tests/YYYY-MM-DD-e2e-results.md`** — see Artifact Standard.

## Completion Report
Report status using exactly one of:
- **DONE** — all main-flow E2E tests PASS; all boundary conditions validated. Proceeding to `/s6-test-perf`.
- **BLOCKED** — list each failing main-flow test with the user journey step that fails.
- **NEEDS_CONTEXT** — E2E test environment not configured; state what is missing.
</what-to-do>
<supporting-info>
## Artifact Standard
Output file: `docs/tests/YYYY-MM-DD-e2e-results.md`

Required sections:
- **Summary**: total flows tested, passed, failed
- **AC Traceability**: for each AC-N.M from Stage 2, which E2E test covers it
- **Main Flows** (PASS / FAIL per flow): use the flow names from `CONTEXT_SNAPSHOT.md`
- **Secondary Flows** (PASS / DEFERRED per flow, with user approval noted if deferred)
- **Failures** (if any): step in user journey that fails, screenshot or log excerpt

## Role Identity: QA Engineer
- **Mindset**: User proxy. If the user can break it, you must find it first.
- **Upstream Dependency**: `/s6-test-integration`.
- **Downstream Target**: `/s6-test-perf`.
## Process Flow

```dot
digraph test_e2e {
    rankdir=TD;
    load     [label="1. Load User Flows\n(CONTEXT_SNAPSHOT)", shape=box];
    map      [label="2. Map flows to\nAC-N.M criteria", shape=box];
    run      [label="3. Run E2E suite\n(Playwright / Cypress)", shape=box];
    main     [label="Main flow\npasses?", shape=diamond];
    second   [label="4. Check secondary\nflows", shape=box];
    all_pass [label="All secondary\npass?", shape=diamond];
    done     [label="DONE → /s6-test-perf", shape=doublecircle];
    blocked  [label="BLOCKED\nmain flow failure", shape=doublecircle];
    concerns [label="DONE_WITH_CONCERNS\nlog secondary failures", shape=doublecircle];

    load -> map;
    map -> run;
    run -> main;
    main -> blocked [label="no — stop"];
    main -> second [label="yes"];
    second -> all_pass;
    all_pass -> done [label="yes"];
    all_pass -> concerns [label="no"];
}
```

</supporting-info>
