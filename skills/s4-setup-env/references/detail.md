# s4-setup-env: Detailed Reference

## Role Identity: Implementer
- **Mindset**: Clean workbench. You don't start coding until the tools are sharp and the environment is pristine.
- **Upstream Dependency**: Stage 3 (Task DAG).
- **Downstream Target**: `/s4-impl-task` & `/s4-tdd`.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s4-setup-env/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Process Flow

```dot
digraph setup_env {
    rankdir=TD;
    select   [label="1. Select Task\nfrom TASK_DAG.md", shape=box];
    branch   [label="2. Checkout\nfeature branch", shape=box];
    runtime  [label="Runtime matches\nRULES.md?", shape=diamond];
    install  [label="3. Install deps\n(pinned versions)", shape=box];
    clean    [label="Workspace clean?\n(no leftover state)", shape=diamond];
    ready    [label="4. Environment\nREADY", shape=box];
    done     [label="DONE → /s4-impl-task\n& /s4-tdd", shape=doublecircle];
    blocked  [label="BLOCKED\nfix runtime", shape=doublecircle];

    select -> branch;
    branch -> runtime;
    runtime -> install [label="yes"];
    runtime -> blocked [label="no — mismatch"];
    install -> clean;
    clean -> ready [label="yes"];
    clean -> install [label="no — clean first"];
    ready -> done;
}
```
