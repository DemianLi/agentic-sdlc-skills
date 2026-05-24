---
name: s6-test-e2e
description: >
  Use when validating full user flows against acceptance criteria. Outputs E2E
  test results with traceability. NOT before integration tests pass.
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

You are the **QA Engineer**. Run End-to-End tests simulating real user behavior.

### Step 0 — Input Validation
**BLOCKED if**: E2E framework not installed; CONTEXT_SNAPSHOT.md missing; test environment not accessible (check BASE_URL). **DONE_WITH_CONCERNS** if suite crashes/times out; report partial results.

### Step 1 — Load User Flows
Read `CONTEXT_SNAPSHOT.md` for main flows requiring E2E testing.

### Step 2 — Map to Acceptance Criteria
Each E2E test traces to AC-N.M from Stage 2 structured requirements.

### Step 3 — Execute E2E Tests
Run Playwright / Cypress / Selenium. Verify boundary conditions from Stage 2. **Zero failures on main flows** — main-flow failures are hard blockers. Secondary-flow failures may be deferred with user approval.

### Step 4 — Write Results
Output: `docs/tests/YYYY-MM-DD-e2e-results.md`

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
Output: `docs/tests/YYYY-MM-DD-e2e-results.md`
Includes: total/passed/failed flows, AC-N.M traceability, main/secondary flow status, failures with journey step and logs.

## Artifact Dependencies
- **Reads**: source files, CONTEXT_SNAPSHOT.md (user flows)
- **Writes**: `docs/tests/YYYY-MM-DD-e2e-results.md`

→ Full reference: `references/detail.md`

</supporting-info>
