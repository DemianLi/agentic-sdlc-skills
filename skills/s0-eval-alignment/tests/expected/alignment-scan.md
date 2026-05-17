## Alignment Scan Report (Fixture Smoke Test)
**掃描範圍**: `tests/fixtures/`（2 個 fixture）
**Date**: (任意日期)
**Evaluator**: s0-eval-alignment
**基線**: `references/skill-design-intent.md`

---

### 總覽表

| Skill | QA Step | Q 對齊 | C1 強制執行 | C2 工件鏈 | C3 Description | 整體 |
|-------|---------|--------|------------|----------|----------------|------|
| `fixture-aligned` | 2.1 | ✅ ALIGNED | ✅ PASS | ✅ PASS | ✅ PASS | ✅ ALIGNED |
| `fixture-drifted` | — | ❌ DRIFTED | ❌ FAIL | ❌ FAIL | ❌ FAIL | ❌ DRIFTED |

---

### 漂移清單

#### `fixture-drifted` — ❌ DRIFTED

- **Q 對齊**：無法對應任何 QA.md 步驟；description 描述「code 任務」而非任何 SDLC 階段關鍵詞
- **C1**：缺少 `<HARD-GATE>` 區塊
- **C2**：`<supporting-info>` 缺失；無 Reads / Writes 聲明
- **C3**：description 含 "Step 1"、"Step 2"、"Step 3" — 摘要了流程而非觸發條件

---

### 優先修復建議

1. `fixture-drifted`：補充 `<HARD-GATE>` + "Awaiting your approval" 尾句
2. `fixture-drifted`：補充 `<supporting-info>` 與工件鏈聲明
3. `fixture-drifted`：修改 description 為觸發條件格式（"Use when..."）
4. `fixture-drifted`：確認此 skill 屬於哪個 QA.md 步驟，補充對應關鍵詞

---

**總計**：1/2 ALIGNED，1/2 DRIFTED

---
<!-- 此檔為 s0-eval-alignment 的 smoke test 期望輸出 -->
<!-- 若實際輸出與此有差異，視為 alignment-inspector drift，需重新校準 -->
