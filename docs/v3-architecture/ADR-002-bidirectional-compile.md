# ADR-002: 工件合約雙向編譯與零漂移架構 (Bidirectional Spec Sync)

**優先級**: P2
**設計來源**: OpenSpec 倉庫哲學 + `skill_graph_3_0_design_dimensions.md` 維度 2
**狀態**: ✅ 已實作 — PR #9 (`feat/p2-bidirectional-compile`，已合入 main)

---

## Context

V2.2 中，`skill_graph_schema.yaml` 與 `README.md` 之間是**單向、被動**的關係：
- 人工維護 schema → 人工更新 README 的文字描述
- 無機制偵測兩者是否已漂移（README 宣稱某依賴，YAML 不這麼說）
- 新增 skill 時，scaffolding 完全手工：複製 SKILL.md 模板、更新 README 表格、更新 SKILL_INDEX.yaml — 三處需同步，任一漏掉即造成漂移

**根本問題**：YAML 和文件不是 Single Source of Truth，而是兩份各自漂移的副本。

---

## Decision

新增兩個 CLI 子命令到 `engine.py`，實作雙向同步：

### 正向編譯：`--sync-docs`

YAML 為主源，自動更新文件：

```bash
python3 skills/s0-eval-alignment/scripts/engine.py --sync-docs
```

**行為**：
1. 讀取 `skill_graph_schema.yaml`，取出所有節點的 `requires / outputs`
2. 重新生成 `README.md` 中的 Mermaid DAG（以 `<!-- SKILL-GRAPH-START -->` / `<!-- SKILL-GRAPH-END -->` 標記包圍，防止覆蓋周圍文字）
3. 為每個在 schema 有但 `skills/` 目錄缺少 `SKILL.md` 的節點，自動創建 scaffold：
   ```
   skills/{node_id}/SKILL.md  ← 含標準 Reads/Writes 模板 + 空 <what-to-do> block
   ```
4. 更新 `SKILL_INDEX.yaml` 的 skill name 列表（不覆蓋 keyword，只補缺失的 skill value）

**Mermaid DAG 生成規則**：
- Stage 1–7 用 `subgraph stageN[Stage N]` 包圍
- HARD-GATE 節點（`s1-lock-tech-stack`、`s2-snapshot-ctx` 等）以 `style nodeId fill:#f96` 標記
- Stage-0 節點放在 `subgraph stage0[Stage 0 — Standalone]` 外部獨立方塊

### 逆向同步：`--lint-drift`

文件與 YAML 互相校驗，偵測漂移：

```bash
python3 skills/s0-eval-alignment/scripts/engine.py --lint-drift
```

**行為**：
1. 解析 `README.md` 的 Mermaid DAG 標記區塊，提取節點 ID 和邊（`A --> B`）
2. 與 `skill_graph_schema.yaml` 的 `requires` 圖對比
3. 若有差異，拋出 `DriftViolationError` 並列出所有不一致項，exit 1（CI 友善）

**Mermaid 解析策略**：
- 正則提取 `A --> B`、`A --text--> B`、`A --- B` 三種 edge 語法
- 跳過 `style`、`classDef`、`subgraph`、`%%` 行
- 若 Mermaid 語法解析失敗 → `DriftViolationError: Mermaid block malformed`（不靜默跳過）

---

## Consequences

**正面**：
- 人工更新三處 → 只改 YAML，`--sync-docs` 自動同步其他
- `--lint-drift` 作為 CI 新增 step，在文件被人工改壞時攔截合併

**負面/風險**：
- Mermaid 逆向解析涉及 regex，複雜 DAG 可能解析失敗 → 採保守策略：解析失敗時 `--lint-drift` 輸出警告但不 exit 1（`--strict-lint` flag 才強制）
- `--sync-docs` 重新生成 Mermaid 會覆蓋任何人工美化的標記區塊 → 必須在文件中明確標注「此區塊由工具自動生成，請勿手動修改」

---

## Verification Plan

### 正向同步測試

```bash
# 1. 在 skill_graph_schema.yaml 加一個測試節點 s9-future-task
# 2. 運行 --sync-docs
python3 skills/s0-eval-alignment/scripts/engine.py --sync-docs
# 3. 斷言
grep -l "s9-future-task" README.md       # Mermaid 中出現
ls skills/s9-future-task/SKILL.md        # scaffold 被自動創建
```

### 漂移偵測測試

```bash
# 1. 故意修改 README.md Mermaid 標記區塊，改掉一條邊
# 2. 運行 --lint-drift
python3 skills/s0-eval-alignment/scripts/engine.py --lint-drift
# 預期：exit 1 + 列出 DriftViolationError
echo $?  # 應為 1
```

### 6 指標框架核對

根據 [[reference_skill_checklist.md]] 第 6 項「長效維護（Drift Monitoring）」：
- `--lint-drift` 即為此處所述的「離線 Eval Set」機制的文件層版本
- CI 中加入 `--lint-drift` step → 防止長期漂移在某次 merge 後靜默累積
