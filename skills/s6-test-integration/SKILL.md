---
name: s6-test-integration
description: >
  Use when verifying cross-module behavior at API boundaries. Outputs integration
  test results and traceability matrix. NOT before all Atomic Tasks are merged.
---
<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)

1. Does `TASK_DAG.md` exist?
   - **No** → run `python skills/s0-eval-alignment/scripts/engine.py --suggest TASK_DAG.md`, report its output, and **STOP**.

Only proceed when TASK_DAG.md is present.

---

Do NOT proceed to `/s6-test-e2e` if any integration test is failing.
Every integration test failure must be reported as a BLOCKER.
3. The integration test results must be machine-generated from actual test execution — a manually created test report does NOT satisfy this gate.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s6-test-e2e.
Do NOT skip /s6-test-e2e’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **QA Engineer**. Test module-to-module behavior at boundaries.

### Step 0 — Input Validation
**BLOCKED if**: `TASK_DAG.md` missing; TASK_DAG.md invalid; test framework not installed; feature branches not merged to integration.

### Step 1 — Verify All Tasks Merged
Confirm all TASK-N in `TASK_DAG.md` marked `[x]`. Run: `git log --oneline | head -20` and `git branch --merged | grep task`.

### Step 2 — Build Traceability Map
For each REQ-N, identify which integration test covers cross-component behavior.

### Step 3 — Run Integration Tests
Execute tests covering API endpoints, database connections, external service calls together. Flag coverage < 75% as **WARNING** for Stage 4 backfill.

### Step 4 — Write Results
For each failing test: name, expected behavior, actual behavior, component boundary. Zero tolerance — all tests must **PASS** before E2E.

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| 在本地測過了，CI 應該也會過 | 本地環境通常和 CI 差別大；沒有完整的 integration test suite run，無法確保相同的結果 |
| 只有 1 個 path 沒過，其他都好 | 1 個 critical path fail 就要停止進展；critical path 定義在 REQ，漏掉它會延伸到 E2E 和部署 |
| 環境依賴不完整，下一個階段再補 | integration test 必須驗證 module 邊界；邊界驗證不了就無法往下進，不是「稍後補」的事 |

## Completion Report
Report status using exactly one of:
- **DONE** — all integration tests PASS; all critical paths from REQ acceptance criteria are covered. Proceeding to `/s6-test-e2e`.
- **BLOCKED** — list each failing test with the component boundary where integration fails.
- **NEEDS_CONTEXT** — integration environment not configured; state what is missing.
</what-to-do>
<supporting-info>

## Artifact Standard
Output: `docs/tests/YYYY-MM-DD-integration-results.md`
Includes: total/passed/failed/skipped tests, REQ-N traceability, coverage %, failures (test name, boundary, expected vs. actual).

## Artifact Dependencies
- **Reads**: source files, docs/specs/YYYY-MM-DD-<topic>-requirements.md, TASK_DAG.md
- **Writes**: `docs/tests/YYYY-MM-DD-integration-results.md`

→ Full reference: `references/detail.md`

</supporting-info>
