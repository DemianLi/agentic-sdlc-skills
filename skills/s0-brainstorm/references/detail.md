# s0-brainstorm: Extended Reference

## Role Identity: Problem Scout
- **Mindset**: Anthropologist, not architect. You observe and reflect — you do not prescribe. The moment you propose a solution, you've stopped brainstorming. A good Problem Scout leaves the session with a crisper problem, not a plan.
- **Upstream Dependency**: None. This skill starts from zero.
- **Downstream Target**: `/s2-capture-vision` — but only if the user chooses to proceed. The draft is a standalone artifact, not a pipeline trigger.

## Semantic Boundary

| Skill | 用途 | 差別 |
|-------|------|------|
| `s0-brainstorm` | 從模糊感覺發現問題陳述 | 無 spec 輸入；輸出是問題，不是方案 |
| `s2-capture-vision` | 從問題陳述建立 PRD | 輸入已是明確問題；輸出是功能需求列表 |
| `s0-trace-feature` | 驗證現有 spec 的功能完整性 | 輸入是已存在的 spec；做驗證，不做探索 |

## Why s0 (Not s2-pre)

This skill is outside the s1–s7 pipeline by design. The pipeline assumes you know what you're building. `s0-brainstorm` is for when you don't. Running it doesn't commit you to building anything — the output is a problem statement, not a plan.

## Process Flow

```dot
digraph brainstorm {
    rankdir=TD;
    listen   [label="1. Empty the Container\n(listen, reflect back)", shape=box];
    visual   [label="2. Visual Questions\n(2-3 questions, one at a time)", shape=box];
    map      [label="3. Map Problem Space\n(who / frequency / cost / workaround)", shape=box];
    frame    [label="4. Generate 3 Framings\n(User Pain / System / Abstraction)", shape=box];
    check    [label="5. Reality-Check\n(symptom? already solved? worth it?)", shape=box];
    choose   [label="User chooses\none framing?", shape=diamond];
    reframe  [label="Reframe entirely", shape=box];
    write    [label="6. Write\nproblem-draft.md", shape=box, style=filled, fillcolor="#cce0ff"];
    done     [label="DONE\n(user decides next step)", shape=doublecircle];
    blocked  [label="BLOCKED\nno framing viable", shape=doublecircle, style=filled, fillcolor="#ffcccc"];

    listen -> visual;
    visual -> map;
    map -> frame;
    frame -> check;
    check -> choose;
    choose -> write [label="yes"];
    choose -> reframe [label="none fit"];
    reframe -> frame;
    write -> done;
    check -> blocked [label="all framings\nrejected"];
}
```

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-brainstorm/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

Smoke test: Confirm skill output structure and behavior match expected_behavior for each scenario.
