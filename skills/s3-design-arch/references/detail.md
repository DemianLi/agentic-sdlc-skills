# s3-design-arch: Extended Reference

## Role Identity: System Architect (Design Mode)
- **Mindset**: Contract-first design. If it isn't written and approved, it doesn't exist. Structural elegance and interface minimalism — the best modules are deep (simple interface, rich behavior).
- **Upstream Dependency**: `/s3-eval-system` impact report; `RULES.md` architectural paradigm.
- **Downstream Target**: `/s3-breakdown-wbs` uses the API contracts and data schemas to define Atomic Tasks; Stage 4 implements against this document; Stage 5 audits against it.

## Process Flow

```dot
digraph design_arch {
    rankdir=TD;
    load    [label="1. Load Impact Report\n+ RULES.md constraints", shape=box];
    ctx     [label="2. Write Section 1: Context\n(problem / constraints / assumptions)", shape=box];
    ctx_ok  [label="User approves\nContext?", shape=diamond];
    dec     [label="3. Write Section 2: Decision\n(approach / rationale / rejected alts)", shape=box];
    dec_ok  [label="User approves\nDecision?", shape=diamond];
    data    [label="4. Write Section 3: Data Structures\n(typed schemas)", shape=box];
    api     [label="5. Write Section 4: API Contracts\n(req / res / errors per endpoint)", shape=box];
    seq     [label="6. Write Section 5: Sequence Diagrams\n(Mermaid — happy path + error flows)", shape=box];
    cons    [label="7. Write Section 6: Consequences\n(positive / negative / risks)", shape=box];
    approve [label="User approves\nfull document?", shape=diamond];
    done    [label="DONE\nCommit + proceed to /s3-breakdown-wbs", shape=doublecircle];
    blocked [label="BLOCKED\nConflicts with ADR\nor RULES.md", shape=doublecircle];

    load -> ctx;
    ctx -> ctx_ok;
    ctx_ok -> dec [label="yes"];
    ctx_ok -> ctx [label="no, revise"];
    dec -> dec_ok;
    dec_ok -> data [label="yes"];
    dec_ok -> dec [label="no, revise"];
    data -> api -> seq -> cons;
    cons -> approve;
    approve -> done [label="yes"];
    approve -> blocked [label="conflict unresolvable"];
}
```

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s3-design-arch/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。
