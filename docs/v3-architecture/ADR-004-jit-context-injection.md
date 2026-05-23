# ADR-004: 極致上下文即時注入 (Just-In-Time Context Injection)

**優先級**: P3
**設計來源**: Matt Pocock Skills 倉庫哲學 + `skill_graph_3_0_design_dimensions.md` 維度 3
**狀態**: ✅ 已實作 — commit `6b8218f` (`feat/p4-jit-context`，已合入 main)

---

## Context

V2.2 中，AI 加載技能時是靜態全量載入：所有 34 個技能的 SKILL.md 可能同時出現在上下文中（取決於 Claude Code 的 skill loading 策略）。即使透過 `SKILL_INDEX.yaml` 做到 O(1) 路由後，仍然需要讀取目標技能的完整文本。

但更深層的問題在**執行期**：

- AI 正在執行 `s4-impl-task`，卻仍「記得」`s3-design-arch` 的架構規則
- 終端顯示 `ValueError: Invalid schema`，AI 的上下文中卻還夾雜著 `s7-telemetry` 的發布步驟
- 這些無關內容消耗 Token，更重要的是可能干擾 AI 的注意力，導致「語義雜訊」

**根本問題**：AI 不需要知道「整個地圖」，它只需要知道「當前腳下的路」。

---

## Decision

引入 **JIT Context Injection** 機制，根據當前 IDE/工作區狀態，動態過濾並注入最小必要上下文。

### 事件感知源（Event Listener）

以**最輕量方式**感知當前活動上下文，優先級由高到低：

1. **`mock_ide.json`**（顯式注入）：用戶或 CI 提供的結構化狀態文件
2. **`.git/index` mtime 比對**：最近被 `git add` 的檔案 → 推斷當前活躍的節點
3. **Workspace sentinel 掃描**：掃描 `.*.done` 和 `.*.rollback` 哨兵，推斷當前節點

活動狀態格式（`mock_ide.json` 示例）：
```json
{
  "active_file": "skills/s0-eval-alignment/scripts/engine.py",
  "last_terminal_output": "ValueError: Invalid schema file format.",
  "active_node_hint": "s4-impl-task"
}
```

### JIT Prompt 生成（`--jit` 子命令）

```bash
python3 skills/s0-eval-alignment/scripts/engine.py --jit --state mock_ide.json
```

**生成流程**：
1. 解析 `active_file` + `last_terminal_output` → 對應到 schema 中的節點
2. 過濾邏輯：
   - **包含**：當前節點的 `reads`、`writes`、`validators`、`requires`（直接上游只）
   - **排除**：其他所有 Stage 的執行步驟
3. 從對應 SKILL.md 提取 `<HARD-GATE>` block 和 `Reads/Writes` 聲明（`<supporting-info>`）
4. 輸出 JIT Prompt（Markdown 格式，注入到下一次 Claude 調用前）

### Token 預算斷言

JIT Prompt 必須滿足：
- Token 大小 < 完整技能集合的 **10%**
- 計算公式：`wc -w jit_output.md` × 1.3（rough token estimate）

### JIT Prompt 緩存清除

當以下任一條件成立時，JIT Prompt 必須重置：
- `--status` 顯示當前節點轉換
- `mock_ide.json` 的 `active_node_hint` 改變
- `--stack-pop`（ADR-003）觸發後

---

## Consequences

**正面**：
- 執行期 Token 消耗降低至 10%（相對完整技能集）
- 減少「語義雜訊」干擾（AI 不會因為看到 s7 的內容而在 s4 做出錯誤決策）
- 與 ADR-003 的 Rollback 機制協同：rollback 時 JIT 自動聚焦在 `rollback_target` 節點

**負面/風險**：
- 節點對應邏輯（`active_file` → node_id）依賴 schema 的 `reads/writes` 欄位 → 必須先完成 ADR-001 的欄位擴展
- `mock_ide.json` 手工維護成本高 → 長期目標是 Claude Code hook 自動注入（超出本 ADR 範圍）
- 過度過濾可能讓 AI 看不到某個關鍵的上游約束 → 保留「展開上游」flag：`--jit --depth 2`（包含兩層上游節點）

---

## Verification Plan

### 模擬 IDE 狀態測試

```bash
# 1. 創建 mock 狀態
cat > /tmp/mock_ide.json << 'EOF'
{
  "active_file": "skills/s0-eval-alignment/scripts/engine.py",
  "last_terminal_output": "ValueError: Invalid schema file format.",
  "active_node_hint": "s4-impl-task"
}
EOF

# 2. 生成 JIT Prompt
python3 skills/s0-eval-alignment/scripts/engine.py --jit --state /tmp/mock_ide.json > /tmp/jit_output.md

# 3. 斷言：不包含 Stage 1, 2, 5, 6, 7 的執行步驟
grep -i "s1-\|s2-\|s5-\|s6-\|s7-" /tmp/jit_output.md && echo "FAIL: contains irrelevant stages" || echo "PASS"

# 4. 斷言：Token 數 < 10% 總量
TOTAL_TOKENS=$(find skills -name "SKILL.md" -exec wc -w {} \; | awk '{sum += $1} END {print sum * 1.3}')
JIT_TOKENS=$(wc -w /tmp/jit_output.md | awk '{print $1 * 1.3}')
python3 -c "assert $JIT_TOKENS < $TOTAL_TOKENS * 0.1, f'JIT too large: {$JIT_TOKENS} >= {$TOTAL_TOKENS * 0.1}'"
```

### 6 指標框架核對

根據 [[reference_skill_checklist.md]] 第 4 項「漸進披露（Progressive Disclosure）」：
- JIT Injection 即為此原則在**執行期**的延伸：不只在路由時省 Token，在整個執行週期都只暴露當前任務所需的最小上下文
- `--depth N` flag 提供漸進展開（從精簡到完整），符合「路由階段只讀精簡大綱」的精神
