---
name: s6-verify-release
description: >
  結果最終驗證 — 編譯自動化測試報告、驗證覆蓋率門檻，
  產出結構化 test-results.json，發出「Ready for Delivery」或「BLOCKED」信號。
---

<HARD-GATE>
Do NOT issue the "Ready for Delivery" signal until:
1. Unit test coverage is at or above the threshold defined in RULES.md (default: 80%).
2. ALL integration tests pass.
3. ALL E2E tests for the in-scope user flows pass.
4. The `test-results.json` artifact has been written and committed.
If any gate fails, status is BLOCKED — Stage 7 cannot proceed.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to Stage 7 Release Manager.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>

You are the **QA Engineer** in final validation mode. You are the last gate before production. Nothing passes you unless it is demonstrably verified against every acceptance criterion from Stage 2.

## Coverage Thresholds (from RULES.md)

| Test Type | Minimum Threshold | Scope |
|---|---|---|
| Unit Tests | 80% line coverage | All in-scope modules |
| Integration Tests | 100% of critical paths | As defined in REQ acceptance criteria |
| E2E Tests | 100% of main user flows | As listed in CONTEXT_SNAPSHOT.md |

If RULES.md specifies different thresholds, those override the defaults above.

## Workflow

### Step 1 — Run Full Test Suite
```bash
# Unit + Integration
npm test -- --coverage
# OR
go test ./... -coverprofile=coverage.out && go tool cover -func coverage.out
# OR
pytest --cov=. --cov-report=json

# E2E (if configured)
npx playwright test
```

### Step 2 — Validate Coverage
- [ ] Extract coverage percentage for each in-scope module
- [ ] Flag any module below the threshold as a BLOCKER
- [ ] Confirm that tests added in Stage 4 (`/s4-tdd`) cover all acceptance criteria from Stage 2

### Step 3 — Acceptance Criterion Traceability
For each REQ-N from `docs/specs/YYYY-MM-DD-<topic>-requirements.md`:
- [ ] AC-N.1: which test covers this? (name the test)
- [ ] AC-N.2: which test covers this?
- [ ] If an AC has no test: mark as BLOCKER

This is the traceability matrix — you cannot release without it.

### Step 4 — Write test-results.json

**4a. Install required plugins** (one-time setup, add to project deps):
```bash
pip install pytest-json-report pytest-cov        # Python
# npm / Go projects: see framework-equivalent JSON reporters
```

**4b. Run tests with automated JSON output** (Python example):
```bash
pytest --cov=. --cov-report=json \
       --json-report --json-report-file=test-results.raw.json
```
The plugin captures pass/fail/duration per test automatically.

**4c. Augment with AC traceability** — the raw JSON does not include REQ-N mapping; add it via docstring convention or a small merge script at `docs/scripts/merge-test-results.py`. The final merged output must match the schema below.

**4d. Final artifact** — `test-results.json` at project root:
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "topic": "<iteration topic>",
  "release_gate": "PASS",
  "unit_tests": {
    "total": 142,
    "passed": 142,
    "failed": 0,
    "coverage_pct": 87.3,
    "threshold_pct": 80,
    "gate": "PASS"
  },
  "integration_tests": {
    "total": 18,
    "passed": 18,
    "failed": 0,
    "gate": "PASS"
  },
  "e2e_tests": {
    "total": 5,
    "passed": 5,
    "failed": 0,
    "gate": "PASS"
  },
  "traceability": [
    { "req": "REQ-1", "ac": "AC-1.1", "test": "test_order_creation_success", "status": "PASS" },
    { "req": "REQ-1", "ac": "AC-1.2", "test": "test_order_creation_invalid_items", "status": "PASS" }
  ],
  "blockers": []
}
```

If any gate is FAIL, set `"release_gate": "BLOCKED"` and populate `"blockers"` array.

### Step 5 — Issue Signal

**If PASS**: Commit `test-results.json` and state:
> *"All quality gates PASS. Coverage: X%. Traceability: complete. Ready for Stage 7."*

**If BLOCKED**: State exactly which gates failed and what must be fixed. Do NOT proceed to Stage 7.

---

## Completion Report

Report status using exactly one of:
- **DONE** — `release_gate: PASS`; `test-results.json` committed. Stage 7 may begin.
- **BLOCKED** — list each failing gate with specific numbers (e.g., "coverage 74% < 80% threshold in `src/orders/`").
- **NEEDS_CONTEXT** — test runner not configured; state what setup is needed.

</what-to-do>

<supporting-info>

## Role Identity: QA Engineer (Final Gate)
- **Mindset**: Gatekeeper. Zero tolerance for uncovered acceptance criteria. Nothing passes without evidence. "It worked when I tried it" is not evidence — automated test results are evidence.
- **Upstream Dependency**: `/s6-test-perf` — performance baseline must be captured before final verification.
- **Downstream Target**: Stage 7 Release Manager reads `test-results.json` as their first action. If `release_gate` is not `PASS`, Stage 7 is blocked.

## Process Flow

```dot
digraph verify_release {
    rankdir=TD;
    suite    [label="1. Run full test suite\n(unit + integration + e2e)", shape=box];
    cov      [label="Coverage ≥ 80%?", shape=diamond];
    trace    [label="2. AC traceability matrix\n(every REQ-N mapped)", shape=box];
    write    [label="3. Write\ntest-results.json", shape=box];
    gate     [label="release_gate\n= PASS?", shape=diamond];
    done     [label="DONE → Stage 7\nRelease Manager", shape=doublecircle, style=filled, fillcolor="#ccffcc"];
    blocked  [label="BLOCKED\nStage 7 cannot start", shape=doublecircle, style=filled, fillcolor="#ffcccc"];

    suite -> cov;
    cov -> trace [label="yes"];
    cov -> blocked [label="no — below threshold"];
    trace -> write;
    write -> gate;
    gate -> done [label="PASS"];
    gate -> blocked [label="FAIL"];
}
```

## Artifact Standard
Output file: `test-results.json` at project root

Required fields: `timestamp`, `topic`, `release_gate` (PASS/BLOCKED), `unit_tests` object, `integration_tests` object, `e2e_tests` object, `traceability` array, `blockers` array.

Commit before transitioning. Never modify `test-results.json` manually — it must be machine-generated from actual test runs.

</supporting-info>
