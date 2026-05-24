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

## Coverage Thresholds

| Test Type | Minimum | Scope |
|---|---|---|
| Unit Tests | 80% line coverage | All in-scope modules |
| Integration Tests | 100% critical paths | REQ acceptance criteria |
| E2E Tests | 100% main user flows | CONTEXT_SNAPSHOT.md |

(RULES.md overrides defaults)

## Workflow

### Step 0 — Pre-flight Check

If any check fails, **stop and report `NEEDS_CONTEXT`**.

| Check | What to verify | Failure |
|---|---|---|
| Test runner | test script in package.json or pytest.ini/go.mod present | BLOCKED: no test runner |
| Test files exist | ≥1 `*.test.*`/`test_*.py`/`*_test.go` | BLOCKED: run `/s4-tdd` |
| Requirements doc | `docs/specs/YYYY-MM-DD-*-requirements.md` present | BLOCKED: no REQ-N/AC |
| Coverage threshold | `RULES.md` %, OR 80% default | Note default if absent |

### Step 1 — Run Full Test Suite

**npm test -- --coverage** OR **pytest --cov=. --cov-report=json** OR **go test ./... -coverprofile=coverage.out**

Run **npx playwright test** if E2E configured.

### Step 2 — Validate Coverage
- [ ] Extract coverage % per in-scope module
- [ ] Flag any module below threshold as BLOCKER
- [ ] Confirm Stage 4 tests cover all Stage 2 ACs

### Step 3 — Acceptance Criterion Traceability

For each REQ-N in requirements doc:
- [ ] AC-N.1: which test covers this? (name it)
- [ ] AC-N.2: which test covers this?
- [ ] If AC has no test: BLOCKER

This traceability matrix is release-critical.

### Step 4 — Write test-results.json

**4a. Install plugins**: **pip install pytest-json-report pytest-cov** (Python; npm/Go equivalents)

**4b. Run with JSON**: **pytest --cov=. --cov-report=json --json-report --json-report-file=test-results.raw.json**

**4c. Augment traceability**: Merge raw JSON with REQ-N mapping via docstring or `docs/scripts/merge-test-results.py`.

**4d. Artifact**: `test-results.json` at root. If any gate FAIL, set **"release_gate": "BLOCKED"** and populate **"blockers"**.

**4e. Example test-results.json**:

Include: `timestamp`, `topic`, `release_gate`, `unit_tests`, `integration_tests`, `e2e_tests`, `traceability`, `blockers`.

### Step 5 — Issue Signal

**If PASS**: Commit & state "All quality gates PASS. Coverage: X%. Ready for Stage 7."

**If BLOCKED**: State which gates failed; list required fixes. Do NOT proceed.

---

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
→ Full reference: `references/detail.md`
</supporting-info>
