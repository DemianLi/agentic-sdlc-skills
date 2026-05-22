# Skill Graph V3.0 Architecture Index

本目錄包含 Skill Graph V3.0 四個維度的架構決策記錄（ADR）。

> **狀態**: 藍圖層（Blueprint）— 設計已確立，實作待後續 PR 分階段落地。
> **設計來源**: `skill_graph_3_0_design_dimensions.md`（Antigravity 端）

---

## V2.2 → V3.0 對照

| 維度 | V2.2 現狀 | V3.0 目標 | 優先級 | ADR |
|:---|:---|:---|:---:|:---|
| **語意驗證** | `sentinel.exists()` + glob 真值 | validators DSL：json_query / regex_match / file_hash | **P1** | [ADR-001](ADR-001-semantic-validation.md) |
| **雙向編譯** | 聲明式 YAML，文件被動 | YAML ⇄ Mermaid/Markdown 雙向同步；scaffolder 自動化 | **P2** | [ADR-002](ADR-002-bidirectional-compile.md) |
| **執行棧 + Rollback** | 靜態 BLOCKED 狀態 | 動態執行棧；局部逆向追蹤修復閉環 | **P3** | [ADR-003](ADR-003-execution-stack-rollback.md) |
| **JIT 上下文注入** | 靜態載入全部技能 | 根據 IDE 活動狀態即時注入 10% 核心提示 | **P3** | [ADR-004](ADR-004-jit-context-injection.md) |

---

## P1/P2/P3 優先級說明

| 優先級 | 理由 | 預估工作量 |
|:---:|:---|:---|
| P1 | 可直接嵌入 `engine.py:_validate_schema`；zero new dependencies；杜絕 AI 規避行為 | 1 PR（~150 行） |
| P2 | `--sync-docs` / `--lint-drift` CLI 新增；腳手架生成；改善開發 DX | 1–2 PR（~300 行） |
| P3 | 需要 IDE 事件監聽或外部 Agent 編排框架支持；最大改動範圍 | 2–3 PR（~500 行） |

---

## 後續 PR 路線圖

```
本 PR (Blueprint)
  ├── schema 補洞（6 Stage-0 節點）
  ├── SKILL_INDEX 新增 s0-semantic-validate
  └── docs/v3-architecture/ + skills/s0-semantic-validate/SKILL.md

下一個 PR (P1 實作)
  ├── engine.py L110: valid_keys 擴展 {validators, reads, writes, sentinels}
  ├── SemanticValidator 類別（json_query / regex_match / file_hash）
  └── tests/test_semantic_validator.py

+2 (P2 實作)
  ├── engine.py: --sync-docs / --lint-drift 子命令
  └── Mermaid 解析器 + scaffolder

+3 (P3 實作)
  ├── .engine_stack.json 持久化
  └── --rollback-trace CLI

+4 (P3 實作)
  ├── JIT prompt 生成器
  └── .git/index 事件感知
```

---

## 核心約束

- **engine.py L110** (`valid_keys = {"stage", "requires", "outputs"}`) 是所有擴展的瓶頸入口，P1 PR 必須先放寬此約束。
- **PyYAML fallback** (`parse_simple_yaml` L20–66) 必須在無 PyYAML 時保持相容。
- **6 指標框架**（[reference_skill_checklist.md](../../../../.claude/projects/-Users-demian-Projects-vibecoding-research-skill-from-github/memory/reference_skill_checklist.md)）每個 ADR 的 Verification Plan 都需引用至少一項。
