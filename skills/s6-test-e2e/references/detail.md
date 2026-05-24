# s6-test-e2e: Detailed Reference

## Role Identity: QA Engineer
- **Mindset**: User proxy. If the user can break it, you must find it first.
- **Upstream Dependency**: `/s6-test-integration`.
- **Downstream Target**: `/s6-test-perf`.

## Eval Fixtures

Fixtures located at `tests/fixtures/s6-test-e2e/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected outcome).

Smoke test: sequentially verify skill output structure and expected_behavior alignment for each scenario.

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
