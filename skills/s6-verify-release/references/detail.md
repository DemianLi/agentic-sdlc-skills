# s6-verify-release — Extended Reference

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

## Eval Fixtures

Fixtures located at `tests/fixtures/s6-verify-release/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected outcome).

Smoke test: confirm skill output structure and expected_behavior alignment for each scenario.
