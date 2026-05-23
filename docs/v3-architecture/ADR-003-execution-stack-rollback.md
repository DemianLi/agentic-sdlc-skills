# ADR-003: 動態執行棧與遞迴自修復閉環 (Execution Stack & Rollback)

**優先級**: P3
**設計來源**: gstack 倉庫哲學 + `skill_graph_3_0_design_dimensions.md` 維度 1
**狀態**: ✅ 已實作 — PR #10 (`feat/p3-rollback-stack`，已合入 main)

---

## Context

V2.2 的失敗處理是靜態的：一旦節點的依賴未完成，它就出現在 `BLOCKED` 清單中，別無其他行動。AI 必須自行決定「要回去修哪個節點」，這個推論過程：

1. **耗費大量 Token**：AI 需要重新分析整個 DAG 和所有相關檔案
2. **容易誤判**：當多個上游節點同時失敗時，AI 可能選錯「罪魁禍首」
3. **無狀態**：中途重啟 Agent 後，失敗上下文完全丟失，從零開始

**根本問題**：真實開發是「前進 → 失敗 → 回溯 → 修復 → 繼續」的動態循環，靜態 BLOCKED 狀態無法表達這個語意。

---

## Decision

引入**動態執行棧（Execution Stack）**，持久化到磁碟，並提供 CLI 介面操作：

### 執行棧資料結構（`.engine_stack.json`）

```json
{
  "active_stack": [
    {
      "node_id": "s6-verify-release",
      "status": "FAILED",
      "failed_at": "2026-05-23T14:30:00Z",
      "failure_reason": "test-results.json: failed=2",
      "rollback_target": "s4-impl-task"
    }
  ],
  "stack_depth": 1,
  "max_depth": 3,
  "last_updated": "2026-05-23T14:30:00Z"
}
```

### 新增 CLI 子命令

```bash
# 顯示當前執行棧
python3 engine.py --stack

# 觸發 rollback trace（分析失敗節點，壓棧修復任務）
python3 engine.py --rollback-trace

# 宣告修復完成，彈棧並繼續
python3 engine.py --stack-pop
```

### Rollback Trace 演算法

1. **偵測失敗節點**：讀取 validators 結果（ADR-001 的 SemanticValidator 輸出）
2. **逆向追蹤最鄰近修改**：
   - 優先用 **mtime 比對**：取失敗工件的 mtime，找所有 `outputs` 中比它更新的上游節點
   - 次選用 **圖最短路徑（BFS）**：從失敗節點向上找最近的 `requires` 節點
3. **壓棧**：將修復目標節點壓入 `active_stack`，同時在 workspace 建立哨兵：
   ```
   .{target_node_id}.rollback   ← 標記「此節點正在修復中」
   ```
4. **上下文鎖定**：輸出精簡的 JIT prompt，只包含 `rollback_target` 節點的 `reads/writes/validators`（引用 ADR-004 的 JIT 機制）
5. **彈棧條件**：當 validators 重新通過 → `--stack-pop` 清除 `.rollback` 哨兵並從 `active_stack` 移除

### 回溯深度限制

- `max_depth: 3`（超過三層不再繼續自動壓棧，改為輸出 `ROLLBACK_LIMIT_EXCEEDED` 並要求人工介入）
- 防止無限遞迴修復迴圈

---

## Consequences

**正面**：
- 修復期間 AI 的上下文聚焦在單一局部，大幅節省 Token
- Agent 重啟後讀取 `.engine_stack.json` 即可恢復上下文，不需重新推論整個 DAG
- `.rollback` 哨兵讓「正在修復中」的狀態對人類可見

**負面/風險**：
- `.engine_stack.json` 必須在 `.gitignore` 中排除（工作區狀態，非 repo 資產）
- mtime 比對在 `git checkout` 後可能全部重置 → 退化為 BFS（保持相容但精度降低）
- `max_depth: 3` 的硬限制可能過保守 → 作為可配置選項（`--max-rollback-depth N`）

---

## Verification Plan

### 模擬故障測試

```bash
# 1. 手動寫入失敗報告
echo '{"summary": {"failed": 2}}' > test-results.json

# 2. 觸發 rollback trace
python3 skills/s0-eval-alignment/scripts/engine.py --rollback-trace

# 3. 斷言
cat .engine_stack.json | python3 -c "import json,sys; d=json.load(sys.stdin); assert len(d['active_stack']) > 0"
ls .s4-impl-task.rollback   # rollback 哨兵應存在

# 4. 修復後彈棧
echo '{"summary": {"failed": 0}}' > test-results.json
python3 skills/s0-eval-alignment/scripts/engine.py --stack-pop
ls .s4-impl-task.rollback 2>/dev/null && echo "FAIL" || echo "PASS"  # 哨兵應消失
```

### 6 指標框架核對

根據 [[reference_skill_checklist.md]] 第 5 項「優雅降級（Fallback）」：
- Rollback Trace 本身即為系統失敗時的優雅降級路徑
- `ROLLBACK_LIMIT_EXCEEDED` 作為「無論如何都能返回的安全保底」，符合 Fallback 定義
