# s5-pr-review: Extended Reference

## Role Identity: Code Auditor (Peer Review Mode)
- **Mindset**: Constructive critic with a concrete voice. You aim to elevate code quality through specific, actionable feedback. No vague comments. No "consider refactoring." Every comment names the file, line, and exact fix.
- **Upstream Dependency**: `/s5-audit-rules` — SAST must be clean before human review.
- **Downstream Target**: `/s5-fix-optimize` — receives the review report and implements fixes.

## Process Flow

```dot
digraph pr_review {
    rankdir=TD;
    scope   [label="1. Scope Drift Detection\n(TASK_DAG vs git diff --stat)", shape=box];
    drift   [label="Scope drift\ndetected?", shape=diamond];
    logic   [label="2. Logic Review\n(API contract / error handling /\nedge cases / naming / N+1)", shape=box];
    sec     [label="3. Security Spot-Check\n(input validation / parameterized queries /\nenv secrets / auth checks)", shape=box];
    report  [label="4. Format Report\n(CRITICAL / WARNING / SUGGESTION\n+ Confirmed Good)", shape=box, style=filled, fillcolor="#cce0ff"];
    has_crit[label="CRITICAL\nissues found?", shape=diamond];
    ack     [label="User acknowledges\nreport?", shape=diamond];
    done    [label="DONE — APPROVED\nProceed to /s5-fix-optimize", shape=doublecircle];
    changes [label="DONE_WITH_CONCERNS\nCHANGES REQUIRED", shape=doublecircle];
    blocked [label="BLOCKED\nScope drift requires\nStage 3 re-scoping", shape=doublecircle];

    scope -> drift;
    drift -> blocked [label="yes — critical drift"];
    drift -> logic [label="clean"];
    logic -> sec -> report;
    report -> has_crit;
    has_crit -> changes [label="yes (blocking)"];
    has_crit -> ack [label="no CRITICALs"];
    ack -> done [label="yes"];
}
```

## Eval Fixtures

Fixtures located at `tests/fixtures/s5-pr-review/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected outcome).

Smoke test: sequentially verify skill output structure and expected_behavior alignment for each scenario.
