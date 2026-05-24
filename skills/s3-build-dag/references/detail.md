# s3-build-dag — Extended Reference

## Role Identity: System Architect (Orchestration Mode)
- **Mindset**: Optimize for concurrent delivery while respecting hard dependencies. Every hour saved in Stage 4 through smart parallelism is an hour of engineering time returned to the user.
- **Upstream Dependency**: `/s3-breakdown-wbs` — the full task list with dependencies.
- **Downstream Target**: Stage 4 Implementer reads `TASK_DAG.md` as their first action. The checklist `[ ]` boxes are the Agent's progress tracker.

## Semantic Boundary

| Skill | 用途 | 差別 |
|-------|------|------|
| `s3-build-dag` | 根據 Atomic Tasks 建立執行 DAG，計算關鍵路徑與並行機會 | 定義「什麼順序、哪些可並行」；不改任務內容 |
| `s3-breakdown-wbs` | 拆解 OpenSpec 為 Atomic Tasks | 定義「做什麼」；不管執行順序 |
| `s4-impl-task` | 執行 DAG 中的單一 Atomic Task | 消費 TASK_DAG.md；不建立 DAG |
| `s3-design-arch` | 設計技術方案與接口 | 更前置；輸出設計文件，不排序任務 |

## Process Flow

```dot
digraph build_dag {
    rankdir=TD;
    load     [label="1. Load Atomic Tasks\n(TASK_DAG.md stub)", shape=box];
    deps     [label="2. Identify Dependencies\nfor each task", shape=box];
    graph    [label="3. Build DAG\n(topological order)", shape=box];
    cycle    [label="Cycle detected?", shape=diamond];
    path     [label="4. Compute Critical Path\n& parallel groups", shape=box];
    approve  [label="User approves\nDAG?", shape=diamond];
    commit   [label="5. Commit\nfinal TASK_DAG.md", shape=box];
    done     [label="DONE → Stage 4", shape=doublecircle];
    blocked  [label="BLOCKED\nresolve cycle", shape=doublecircle];

    load -> deps;
    deps -> graph;
    graph -> cycle;
    cycle -> blocked [label="yes"];
    cycle -> path [label="no"];
    path -> approve;
    approve -> commit [label="yes"];
    approve -> deps [label="revisions"];
    commit -> done;
}
```

## Artifact Standard

Output file: `TASK_DAG.md` at project root (not in `docs/` — it is the active execution guide)

Required sections:
- Mermaid graph with time annotations on each node
- Critical Path calculation
- Parallel Opportunities list
- Execution Checklist with `[ ]` boxes

Commit before transitioning.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s3-build-dag/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。
