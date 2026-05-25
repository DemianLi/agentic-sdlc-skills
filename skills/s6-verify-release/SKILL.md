---
name: s6-verify-release
description: >
  Use when issuing release gate decision (PASS/BLOCKED) in test-results.json. Outputs
  traceability matrix, coverage, blockers. NOT for individual test runs.
---
<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s6-verify-release`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT issue "Ready for Delivery" until:
1. Unit test coverage ≥ threshold in RULES.md (default: 80%).
2. ALL integration tests pass.
3. ALL E2E tests for in-scope flows pass.
4. `test-results.json` written & committed (machine-generated, NOT manual).
If any gate fails: BLOCKED — Stage 7 cannot proceed.

After presenting the artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed to Stage 7 Release Manager."
</HARD-GATE>
<what-to-do>
You are the **QA Engineer** in final validation mode—the last gate before production.

**Coverage Thresholds**: Unit ≥80%, Integration/E2E 100% per RULES.md. Verify test runner, files, REQ docs exist before running.
→ Thresholds table: `references/s6-verify-release-thresholds.md`

### Step 1 — Run Full Test Suite
`npm test -- --coverage` / `pytest --cov=. --cov-report=json` / `go test ./... -coverprofile=coverage.out`
Run `npx playwright test` if E2E configured.

### Step 2 — Validate Coverage
- [ ] Extract coverage % per in-scope module
- [ ] Flag any module below threshold as BLOCKER
- [ ] Confirm Stage 4 tests cover all Stage 2 ACs

### Step 3 — Acceptance Criterion Traceability
For each REQ-N in requirements doc:
- [ ] Map each AC-N.M to its test (name it); if no test: BLOCKER
This traceability matrix is release-critical.

### Step 4 — Write test-results.json
Machine-generated only (never manual). Include: `timestamp`, `topic`, `release_gate`, `unit_tests`, `integration_tests`, `e2e_tests`, `traceability`, `blockers`.
→ JSON spec & commands: `references/s6-verify-release-json-spec.md`

### Step 5 — Issue Signal
**PASS**: Commit & state "All quality gates PASS. Coverage: X%. Ready for Stage 7."
**BLOCKED**: State which gates failed; list required fixes. Do NOT proceed.

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| I'll manually fill test-results.json, numbers are correct | Manual files cannot be audited; if issues arise post-deploy, you cannot prove what was tested |
| Coverage 79% is close enough | Gate threshold is set in RULES.md — 1% short is FAIL. Thresholds exist to be enforced, not suggested. |
| No traceability matrix but coverage looks good | Traceability is a legal document. "Looks good" is not evidence. Every AC-N.M must map to a test case. |

## Completion Report

- **DONE** — `release_gate: PASS`; `test-results.json` committed. Stage 7 may begin.
- **BLOCKED** — list each failing gate with numbers (e.g., "coverage 74% < 80% in `src/orders/`").
- **NEEDS_CONTEXT** — test runner not configured; state what setup is needed.
</what-to-do>

<supporting-info>

**Reads**: docs/tests/YYYY-MM-DD-integration-results.md, docs/tests/YYYY-MM-DD-e2e-results.md, docs/tests/YYYY-MM-DD-perf-baseline.json, docs/specs/YYYY-MM-DD-*-requirements.md, RULES.md
**Writes**: test-results.json

## Eval Fixtures

Fixtures located at `tests/fixtures/s6-verify-release/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
