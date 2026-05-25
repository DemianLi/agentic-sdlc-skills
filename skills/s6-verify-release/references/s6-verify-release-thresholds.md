# s6-verify-release — Coverage Thresholds & Pre-flight Checks

## Coverage Thresholds

| Test Type | Minimum | Scope |
|---|---|---|
| Unit Tests | 80% line coverage | All in-scope modules |
| Integration Tests | 100% critical paths | REQ acceptance criteria |
| E2E Tests | 100% main user flows | CONTEXT_SNAPSHOT.md |

RULES.md overrides defaults.

## Pre-flight Checks

| Check | What to verify | Failure |
|---|---|---|
| Test runner | test script in package.json or pytest.ini/go.mod present | BLOCKED: no test runner |
| Test files exist | ≥1 `*.test.*`/`test_*.py`/`*_test.go` | BLOCKED: run `/s4-tdd` |
| Requirements doc | `docs/specs/YYYY-MM-DD-*-requirements.md` present | BLOCKED: no REQ-N/AC |
| Coverage threshold | `RULES.md` %, OR 80% default | Note default if absent |
