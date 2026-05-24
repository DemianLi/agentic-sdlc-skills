# s0-trace-feature: Extended Reference

## Role Identity: Code Archaeologist
- **Mindset**: A geologist, not a critic. You read strata as they are. Record what exists. Do not propose changes, refactors, or improvements.
- **Upstream**: None. This skill is standalone — invoke it any time on any existing codebase.
- **Downstream**: The output `docs/traces/*.md` can feed directly into `/s3-eval-system` (as codebase context for impact assessment) or `/s2-capture-vision` (if the user wants to modify the traced feature next).

## Process Flow Diagram

```dot
digraph trace_feature {
    rankdir=TD;
    scope     [label="1. Feature Scoping\n(ask user for feature name)", shape=box];
    discover  [label="2. Entry Point Discovery\n(scan workspace, list candidates)", shape=box];
    confirm   [label="User confirms\nentry point(s)?", shape=diamond];
    trace     [label="3. Full Chain Trace\n(follow calls, mark gaps & boundaries)", shape=box];
    confcheck [label="4. Confidence Check\nC1 / C2 / C3", shape=diamond];
    warn      [label="Prepend ⚠️ LOW CONFIDENCE\nask: proceed or investigate more?", shape=box, style=filled, fillcolor="#ffe0cc"];
    write     [label="5. Write docs/traces/\ncommit file", shape=box, style=filled, fillcolor="#ccffcc"];
    done      [label="DONE\nReport status", shape=doublecircle];

    scope -> discover;
    discover -> confirm;
    confirm -> trace [label="confirmed"];
    confirm -> discover [label="unclear — rescan"];
    trace -> confcheck;
    confcheck -> warn [label="any condition true"];
    confcheck -> write [label="all clear"];
    warn -> write [label="user says proceed"];
    warn -> trace [label="user says investigate more"];
    write -> done;
}
```

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-trace-feature/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

Smoke test: Confirm skill correctly traces call chains, detects gaps (marking as [?]), confidence-checks for C1/C2/C3 conditions, and generates Mermaid diagram with proper notation.
