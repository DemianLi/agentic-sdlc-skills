# s6-verify-release — test-results.json Spec & Commands

## Commands

**Python**: `pip install pytest-json-report pytest-cov && pytest --cov=. --cov-report=json --json-report --json-report-file=test-results.raw.json`

Augment traceability: Merge raw JSON with REQ-N mapping via docstring or `docs/scripts/merge-test-results.py`.

## Required Fields

`test-results.json` must include:
- `timestamp`
- `topic`
- `release_gate` — `"PASS"` or `"BLOCKED"`
- `unit_tests` — coverage %, pass/fail count
- `integration_tests` — pass/fail count
- `e2e_tests` — pass/fail count
- `traceability` — array of `{ac_id, test_name, status}`
- `blockers` — list of failed gates (empty if PASS)
