---
name: s0-grill
description: >
  Use when stress-testing any plan, design, or proposal before writing code.
  Maps every decision to a full branch tree; no TBD leaves allowed. Standalone —
  works without vision.md. NOT a replacement for /s2-align-req (which is
  pipeline-locked to vision.md and gates to s2-struct-req).
---

<HARD-GATE>
⛔ OUTPUT DISCIPLINE:
After presenting the decision map, your message MUST end with exactly:
  "Awaiting your approval. Ready to proceed — or tell me which branch to re-examine."
Do NOT invoke any pipeline skill automatically.
</HARD-GATE>

<what-to-do>

**Decision Interrogator**: Your job is to find every hidden assumption, unresolved branch, and scope leak in the user's plan — before anyone writes code.

### 絕對不要觸發的情境

| 情境 | 改用 |
|------|------|
| 你已有 vision.md 且進入 Stage 2 pipeline | `/s2-align-req` — pipeline-locked；有下游 gate 到 s2-struct-req |
| 你在探索一個還沒成形的問題 | `/s0-brainstorm` — 問題空間探索；此 skill 需要一個具體計畫 |
| 你想驗證已寫完的 spec 有沒有遺漏 | `/s0-trace-feature` — spec 覆蓋率驗證；非決策衝突挖掘 |

### Step 0 — Input Validation

此 skill 需要一個具體的計畫、設計提案、或功能描述作為輸入。

| 失敗情境 | 行為 |
|---------|------|
| 輸入只有模糊意圖（e.g., "讓它更好"）| 停止：「請提供具體的計畫或設計提案。模糊感覺請改用 `/s0-brainstorm`。」|
| 輸入已是完整的 OpenSpec 設計文件 | 停止：「這已是設計文件；請使用 `/s5-pr-review` 審查已完成設計。」|

### Step 1 — Decompose the Plan

讀取用戶輸入（計畫、提案、或描述）。提取：
- 所有**決策點** — 計畫中明確或隱含的選擇
- 所有**假設** — 明示或暗示的前提
- 所有**邊界案例** — 未提及的情境

列出清單。此步驟不解決，只列舉。

### Step 2 — Decision Tree Expansion

對 Step 1 中每個決策點，展開為完整分支樹：

```
Decision: [問題]
├── Case A: [條件] → [行為]
├── Case B: [條件] → [行為]
└── Case C: [邊界/錯誤] → [行為 或 明確延後理由]
```

規則：
- **不允許 TBD 葉節點** — 每個分支必須有明確結果或帶理由的具名延後
- 每個假設轉為分支："假設 X" → "若 X 為假：[後果]"
- 不允許只有 happy path 的樹

### Step 3 — Resolution Loop

對每個未解決的分支或假設，逐一處理：
1. 清楚陳述衝突或缺口
2. 提出解決方案
3. 詢問：「這符合你的意圖嗎？」
4. 等待回應
5. 標記 `[RESOLVED]`

一次一個。不批量處理。

### Step 4 — Write Decision Map

所有決策解決後，輸出最終決策圖（預設內聯；用戶要求時存為文件）：

```markdown
## Decision Map: [計畫名稱]

### Decisions
[每個決策的完整分支樹，所有葉節點標記 RESOLVED]

### Scope Boundary
- **IN**: [明確包含項目]
- **OUT**: [明確排除項目]
- **Deferred**: [已承認的延後項，含理由與未來迭代]

### Accepted Risks
[用戶接受的風險；明確標記]
```

## Completion Report

- **DONE** — 所有分支已解決；範圍邊界明確；決策圖已輸出。
- **DONE_WITH_CONCERNS** — 已解決，但列出用戶接受的風險（e.g., "auth 延後造成安全暴露面"）。
- **BLOCKED** — 用戶無法解決某個關鍵分支；陳述該分支及所需決策。
- **NEEDS_CONTEXT** — 需要領域專業知識；陳述缺少哪些資訊。

</what-to-do>

<supporting-info>

任何計畫或設計的獨立決策壓力測試 — 無 pipeline 前置條件。

**與 `/s2-align-req` 的區別**：s2-align-req 是 pipeline-locked（讀 vision.md → gate 到 s2-struct-req）；s0-grill 是獨立工具（任何輸入 → 決策圖），兩者使用相同的分支樹技術，並存不衝突。

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-grill/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: 任何計畫、設計提案、或功能描述（內聯文字或文件）
- **Writes**: 決策圖（預設內聯；文件為可選輸出）

</supporting-info>
