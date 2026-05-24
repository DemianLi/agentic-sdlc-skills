# s2-capture-vision — Reference Detail

## Role Identity: Product Manager (Vision Capture)
- **Mindset**: Empathy-driven, business-value focused. Care about the problem, not the solution. YAGNI ruthlessly.
- **Upstream Dependency**: Stage 1 rules must be established (`RULES.md`, `CONTEXT.md`).
- **Downstream Target**: `/s2-align-req` — uses this vision as its baseline.

## Process Flow

```dot
digraph capture_vision {
    rankdir=TD;
    explore   [label="1. Explore context\n(CONTEXT.md, docs, commits)", shape=box];
    scope     [label="2. Assess scope\nSingle or multi-subsystem?", shape=diamond];
    decompose [label="Decompose into\nsub-projects first", shape=box, style=filled, fillcolor="#fff3cc"];
    questions [label="3. Clarify questions\n(ONE at a time)", shape=box];
    approaches[label="4. Propose 2-3 approaches\nwith trade-offs", shape=box];
    sections  [label="5. Present design\nsection by section", shape=box];
    write_doc [label="6. Write design doc\ndocs/specs/YYYY-MM-DD-vision.md", shape=box, style=filled, fillcolor="#cce0ff"];
    self_rev  [label="7. Spec self-review", shape=box];
    user_rev  [label="8. User reviews", shape=box];
    done      [label="9. DONE → /s2-align-req", shape=doublecircle];

    explore -> scope;
    scope -> decompose [label="multi-system"];
    scope -> questions [label="single system"];
    decompose -> questions;
    questions -> approaches;
    approaches -> sections;
    sections -> write_doc;
    write_doc -> self_rev -> user_rev -> done;
}
```

## Eval Fixtures
Fixtures 位於 `tests/fixtures/s2-capture-vision/cases.json`。
每個 fixture 包含：`scenario`、`input`、`expected_behavior`。
