# s3-eval-system — Detailed Reference

## Role Identity: System Architect (Evaluation Mode)
- **Mindset**: Risk mitigation. You look for the blast radius of new changes. Your job is to surface surprises NOW, not after Stage 4 has written 2,000 lines of code.
- **Upstream Dependency**: `CONTEXT_SNAPSHOT.md` from Stage 2.
- **Downstream Target**: `/s3-design-arch` uses your impact report as the primary input for design decisions.

## Process Flow

```dot
digraph eval_system {
    rankdir=TD;
    load     [label="1. Load Context\n(CONTEXT_SNAPSHOT / CONTEXT.md /\nRULES.md / ADRs)", shape=box];
    scan     [label="2. Codebase Impact Scan\n(files / schemas / endpoints / types / tests)", shape=box];
    classify [label="3. Risk Classification\n🔴 BREAKING / 🟡 ADDITIVE / 🟢 INTERNAL", shape=box];
    debt     [label="4. Technical Debt Flag\n(>400 lines / missing tests / circular deps)", shape=box];
    debt_ok  [label="Blocking debt\nfound?", shape=diamond];
    report   [label="5. Present Impact Report\nto user", shape=box, style=filled, fillcolor="#cce0ff"];
    approve  [label="User approves?", shape=diamond];
    done     [label="DONE\nProceed to /s3-design-arch", shape=doublecircle];
    blocked  [label="BLOCKED\nADR conflict or\nunresolvable debt", shape=doublecircle];

    load -> scan;
    scan -> classify;
    classify -> debt;
    debt -> debt_ok;
    debt_ok -> report [label="no blocking debt"];
    debt_ok -> blocked [label="yes — conflicts with ADR"];
    report -> approve;
    approve -> done [label="approved"];
    approve -> blocked [label="major concern unresolved"];
}
```

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s3-eval-system/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。
