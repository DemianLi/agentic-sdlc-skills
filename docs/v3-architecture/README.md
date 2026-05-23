# Skill Graph V3.0 Architecture Index

本目錄包含 Skill Graph V3.0 四個維度的架構決策記錄（ADR）。

> **狀態**: ✅ 全部實作完成 — P1 / P1.5 / P2 / P3 / P4 已合入 main（73 個測試通過）
> **設計來源**: `skill_graph_3_0_design_dimensions.md`（Antigravity 端）

---

## V2.2 → V3.0 對照

| 維度 | V2.2 現狀 | V3.0 實作 | 優先級 | ADR | 狀態 |
|:---|:---|:---|:---:|:---|:---:|
| **語意驗證** | `sentinel.exists()` + glob 真值 | `SemanticValidator`（json_query / regex_match / file_hash）；strict 模式阻斷 | **P1** | [ADR-001](ADR-001-semantic-validation.md) | ✅ |
| **雙向編譯** | 聲明式 YAML，文件被動 | `--sync-docs` / `--lint-drift`；YAML ⇄ Mermaid 雙向；`DriftViolationError` | **P2** | [ADR-002](ADR-002-bidirectional-compile.md) | ✅ |
| **執行棧 + Rollback** | 靜態 BLOCKED 狀態 | `ExecutionStack`；`--rollback-trace`；`.rollback` 哨兵；mtime + BFS 回溯 | **P3** | [ADR-003](ADR-003-execution-stack-rollback.md) | ✅ |
| **JIT 上下文注入** | 靜態載入全部技能 | `--jit --state`；4 優先級訊號感知；10% token 斷言；`--depth N` 展開 | **P4** | [ADR-004](ADR-004-jit-context-injection.md) | ✅ |

---

## 已合入 PR 記錄

| PR | 分支 | 內容 | 測試數 |
|:---:|:---|:---|:---:|
| Blueprint | `feat/v3-blueprint` | schema 補洞（6 Stage-0 節點）；SKILL_INDEX；ADR 骨架；`s0-semantic-validate` | — |
| #8 (P1+P1.5) | `feat/p1-semantic-validator` + `feat/p1.5-file-hash` | `SemanticValidator`（json_query / regex_match / file_hash + SHA256 sentinel） | 45 |
| #9 (P2) | `feat/p2-bidirectional-compile` | `sync_docs` / `lint_drift`；`DriftViolationError`；Mermaid 雙向 | 45→45 |
| #10 (P3) | `feat/p3-rollback-stack` | `ExecutionStack`；`rollback_trace`；`stack_pop`；`.gitignore` 更新 | 59 |
| P4 | `6b8218f` | `generate_jit_prompt`；`_detect_active_node`；`jit_token_check`；`--token-check` | 73 |

---

## 核心約束

- **engine.py L110** (`valid_keys = {"stage", "requires", "outputs"}`) 是所有擴展的瓶頸入口，P1 PR 必須先放寬此約束。
- **PyYAML fallback** (`parse_simple_yaml` L20–66) 必須在無 PyYAML 時保持相容。
- **6 指標框架**（[reference_skill_checklist.md](../../../../.claude/projects/-Users-demian-Projects-vibecoding-research-skill-from-github/memory/reference_skill_checklist.md)）每個 ADR 的 Verification Plan 都需引用至少一項。
