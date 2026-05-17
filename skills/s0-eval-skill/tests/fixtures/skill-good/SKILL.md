---
name: fixture-good
description: >
  示範 Skill — 通過所有 6 項生產級標準的參考實作。
  接受單一輸入（`target_path`），執行靜態分析並輸出報告。
---

<HARD-GATE>
Do NOT auto-proceed to any downstream skill.
After presenting the artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Static Analyzer**. Read files, report findings, do not modify anything.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想*執行*程式碼，不是分析 | `/s4-impl-task` |
| 用戶想*修復*發現的問題 | `/s5-fix-optimize` |

---

## Workflow

### Step 0 — Input Validation

接受唯一輸入：`target_path`（絕對路徑）。

| 失敗情境 | 行為 |
|---------|------|
| 未提供路徑 | BLOCKED — 提問「請提供目標路徑。」 |
| 路徑不存在 | BLOCKED — 回報「`<path>` 不存在。」 |
| 路徑為目錄而非檔案 | PARTIAL — 掃描目錄下所有 `.py` 檔；報告標記 `DIR_MODE` |

### Step 1 — Read Target

讀取 `target_path`。若讀取逾時（> 30s），標記 `NEEDS_CONTEXT — file unreadable`，仍產出空報告框架。

### Step 2 — Analyze

執行靜態分析。若分析工具不可用，降級為文字搜尋並標記 `DONE_WITH_CONCERNS — fallback mode`。

### Step 3 — Write Report

寫入：`docs/analysis/YYYY-MM-DD-<name>-report.md`

### Step 4 — Commit

```bash
git add docs/analysis/
git commit -m "analysis: static report for <name>"
```

---

## Completion Report
- **DONE** — 報告已寫入並提交。
- **DONE_WITH_CONCERNS** — 已降級為 fallback 模式；報告已提交。
- **BLOCKED** — 輸入驗證失敗；說明原因。
- **NEEDS_CONTEXT** — 目標不可讀；已產出空報告框架。

</what-to-do>

<supporting-info>

## Role Identity: Static Analyzer
- **Mindset**: 觀察者，不介入。
- **Upstream Dependency**: 用戶提供的 `target_path`。
- **Downstream Target**: `/s5-fix-optimize`（用戶選擇後）。

## Semantic Boundary

| Skill | 差異 |
|-------|------|
| `/s5-audit-rules` | 審計程式碼對 RULES.md 的合規性；此 skill 做通用靜態分析 |
| `/s5-fix-optimize` | 修復問題；此 skill 只報告不修改 |

## Eval Fixtures

Fixtures 位於 `tests/fixtures/`。PASS 案例與 FAIL 案例各一。
執行 `s0-eval-skill` 對本 fixture 打分可驗證評分邏輯。

## Artifact Dependencies
- **Reads**: `target_path`（用戶提供）
- **Writes**: `docs/analysis/YYYY-MM-DD-<name>-report.md`

</supporting-info>
