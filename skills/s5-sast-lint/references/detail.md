# s5-sast-lint — Detailed Reference

## Role Identity: Code Auditor (SAST Mode)
- **Mindset**: Unforgiving machine. You trust no one. You do not make exceptions for "it's just a warning." A CRITICAL finding blocks the pipeline regardless of deadline pressure.
- **Upstream Dependency**: Stage 4 output — all unit tests must be GREEN before SAST runs.
- **Downstream Target**: `/s5-audit-rules` — only receives code that has passed static analysis.

## Process Flow

```dot
digraph sast_lint {
    rankdir=TD;
    load    [label="1. Load RULES.md\n(linter / formatter / SAST / forbidden patterns)", shape=box];
    fmt     [label="2. Run Formatter\n(Prettier / Black / gofmt)", shape=box];
    lint    [label="3. Run Linter\n(--max-warnings 0)", shape=box];
    triage  [label="4. Classify Findings\n🔴 CRITICAL / 🟡 WARNING / 🟢 INFO", shape=box];
    has_crit[label="CRITICAL\nfindings?", shape=diamond];
    autofix [label="5. Auto-fix safe issues\n(non-behavioral only)", shape=box];
    sast    [label="6. Run SAST\n(semgrep / gosec / bandit)", shape=box];
    sast_ok [label="HIGH/CRITICAL\nSAST findings?", shape=diamond];
    report  [label="7. Generate Report\n(PASS / BLOCKED)", shape=box, style=filled, fillcolor="#cce0ff"];
    done    [label="DONE — PASS\nProceed to /s5-audit-rules", shape=doublecircle];
    blocked [label="BLOCKED\nCRITICAL must be fixed", shape=doublecircle];

    load -> fmt -> lint -> triage;
    triage -> has_crit;
    has_crit -> autofix [label="WARNING/INFO only"];
    has_crit -> blocked [label="yes — cannot auto-fix"];
    autofix -> sast;
    sast -> sast_ok;
    sast_ok -> report [label="clean"];
    sast_ok -> blocked [label="HIGH/CRITICAL found"];
    report -> done;
}
```

## Artifact Standard
Report file: `docs/audit/YYYY-MM-DD-<branch>-sast.md`
Required fields: Status (PASS/BLOCKED), CRITICAL count, WARNING count, Auto-fixed count, Zero Violations Confirmed list.

## Eval Fixtures

Fixtures located at `tests/fixtures/s5-sast-lint/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected outcome).

Smoke test: sequentially verify skill output structure and expected_behavior alignment for each scenario.
