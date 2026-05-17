# TASK_DAG — changelog-checker

## Dependency Graph

```
T1 (parser)
├── T2 (rules R1+R5)
│   └── T8b (test_rules)
├── T3 (rules R2)
│   └── T8b
├── T4 (rules R3)
│   └── T8b
├── T5 (rules R4)
│   └── T8b
└── T8 (test_parser)

T1 + T2..T5 → T6 (reporter) → T7 (cli) → T9 (test_cli)
```

## Critical Path

T1 → T2 → T6 → T7 → T9

## Execution Order (sequential)

1. T1 — parser
2. T8 — test_parser (RED first)
3. T2, T3, T4, T5 — rules (all depend on T1 only, can batch)
4. T8b — test_rules (RED first)
5. T6 — reporter
6. T7 — cli
7. T9 — test_cli (integration)

## Reads / Writes

- **Reads**: `design.md`, `wbs.md`, `RULES.md`, `CONTEXT.md`
- **Writes**: `TASK_DAG.md` (this file)
