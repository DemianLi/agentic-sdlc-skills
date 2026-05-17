---
name: s6-test-e2e
description: >
  Use after /s6-test-integration to validate full user flows and edge cases against
  the acceptance criteria defined in Stage 2.
---
<HARD-GATE>
Do NOT proceed to `/s6-test-perf` if any E2E test covering a main user flow fails.
E2E test failures on main flows are BLOCKING — they cannot be deferred.
3. The e2e test results must be machine-generated from actual test execution — a manually created test report or screenshots does NOT satisfy this gate.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s6-test-perf.
Do NOT skip /s6-test-perf’s own HARD-GATE conditions.
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

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| E2E 是 flaky test，這次失敗不算 | Flaky test 是環境問題或測試邏輯問題，必須在這一關修掉；帶著 flaky 進入 performance 和部署，會被誤判為效能 issue |
| 截圖看起來對，不需要跑完整 suite | 截圖是點狀驗證；E2E suite 是面狀驗證；沒有 suite 結果，無法確認整個 flow 從開始到結束都通 |
| main flow 都過了，secondary 的失敗可以稍後補 | secondary flow fail 累積到部署後被客戶發現，成本是現在修的 100 倍 |

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

## Artifact Dependencies
- **Reads**: source files, `CONTEXT_SNAPSHOT.md` (user flows)
- **Writes**: `docs/tests/YYYY-MM-DD-e2e-results.md`

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
