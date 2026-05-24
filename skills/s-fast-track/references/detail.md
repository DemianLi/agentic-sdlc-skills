# s-fast-track: Extended Reference

## When Fast-Track Is the Wrong Choice

Do not use this skill if any of the following are true:
- The user is starting a brand-new project with no existing codebase
- The task requires coordinating with other agents or teams
- The user is unsure what they want to build (use `/s0-brainstorm` instead)
- The task will touch more than 3 files across different modules
- Compliance, security, or architectural decisions are in scope

## Role Identity: Fast-Track Router
- **Mindset**: Remove friction, not discipline. The goal is to get to s4 faster — not to skip s4's rigor.
- **Upstream Dependency**: None. This is an entry point.
- **Downstream Target**: One of s4-tdd, s4-impl-task, s4-setup-env, or s4-local-debug.

## Process Flow

```
/s-fast-track
  → Mode Signal Detection
      --vibe   → Vibe confirmation (wait Y) → s4-impl-task
      --hotfix → Hotfix announcement       → s4-tdd
      standard → Greenfield Check
                   RULES.md missing → Express Mode (3Q interview → write artifacts) → Routing Table
                   RULES.md exists  → Standard Mode (1 question)                   → Routing Table
```

## Eval Fixtures

Fixtures 位於 `tests/fixtures/fast-track-cases.json`。

每個 fixture 包含：`description`（任務描述）、`expected_mode`（Standard / Vibe / Hotfix）、`expected_route`（目標 skill）。

冒煙測試：逐一對照 fixture 的 `expected_route` 與 skill 實際路由結果是否一致。
