# s4-tdd — Reference Detail

## Role Identity: Implementer (TDD Mode)
- **Mindset**: If you can't write a failing test for it, you don't understand the requirement well enough.
- **Upstream Dependency**: `/s4-setup-env` (environment ready) + Acceptance Criteria from `TASK_DAG.md`.
- **Downstream Target**: `/s4-impl-task` (GREEN tests unlock implementation).

## Process Flow

```dot
digraph tdd_cycle {
    rankdir=LR;
    plan [label="Plan:\nList behaviors\n(await user approval)", shape=box];
    red  [label="RED\nWrite failing test", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="Verify:\ntest FAILS\ncorrectly?", shape=diamond];
    green [label="GREEN\nMinimal code\nto pass", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="Verify:\nALL tests pass?", shape=diamond];
    refactor [label="REFACTOR\nClean up", shape=box, style=filled, fillcolor="#cce0ff"];
    next [label="Next behavior?", shape=diamond];
    done [label="DONE\nReport status", shape=doublecircle];

    plan -> red;
    red -> verify_red;
    verify_red -> green [label="yes"];
    verify_red -> red [label="wrong failure\nfix test"];
    green -> verify_green;
    verify_green -> refactor [label="yes"];
    verify_green -> green [label="no, fix code"];
    refactor -> next;
    next -> red [label="yes"];
    next -> done [label="no"];
}
```

## Eval Fixtures
Fixtures located at `tests/fixtures/s4-tdd/cases.json`.
Each fixture: `scenario`, `input`, `expected_behavior`.
