# s6-test-integration: Detailed Reference

## Role Identity: QA Engineer
- **Mindset**: Boundary breaker. You test the glue between the components. Coverage gate belongs to `/s6-verify-release`, but an early warning here saves a costly Stage 4 round-trip.
- **Upstream Dependency**: Stage 5 Output.
- **Downstream Target**: `/s6-test-e2e`.

## Eval Fixtures

Fixtures located at `tests/fixtures/s6-test-integration/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected outcome).

Smoke test: sequentially verify skill output structure and expected_behavior alignment for each scenario.

## Process Flow

```dot
digraph test_integration {
    rankdir=TD;
    check    [label="1. Verify all TASK-N\nare [x] in DAG", shape=diamond];
    trace    [label="2. Load REQ-N\ntraceability matrix", shape=box];
    run      [label="3. Run integration\ntest suite", shape=box];
    pass_all [label="All tests pass?", shape=diamond];
    write    [label="4. Write results\nto test report", shape=box];
    done     [label="DONE → /s6-test-e2e", shape=doublecircle];
    blocked  [label="BLOCKED\nfail details + owner", shape=doublecircle];

    check -> trace [label="all done"];
    check -> blocked [label="incomplete tasks"];
    trace -> run;
    run -> pass_all;
    pass_all -> write [label="yes"];
    pass_all -> blocked [label="no"];
    write -> done;
}
```
