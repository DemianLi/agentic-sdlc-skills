---
name: s0-eval-alignment
description: >
  Use when verifying s1-s7 skills haven't drifted from design intent. Batch-scans
  all skills, outputs ALIGNED/PARTIAL/DRIFTED. NOT for single-skill audits.
---

<HARD-GATE>
Do NOT edit any skill file during this evaluation.
Do NOT run this skill on a single skill file — use s0-eval-skill for single-skill structural audits.
The only permitted output is a batch alignment report written to disk.

After presenting the report, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Alignment Inspector**. Detect drift between what a skill does now and what it was designed to do.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想評估**單一 skill 的結構品質**（6 項 QA 標準） | `s0-eval-skill` |
| 用戶想**修改**某個 skill 的內容 | `s5-fix-optimize` |
| 用戶想了解**系統整體架構**是否健康 | `s3-eval-system` |

### Step 0 — 確認掃描範圍（s1-s7）

| 失敗情境 | 行為 |
|---------|------|
| `skills/` 不存在 | BLOCKED |
| 某個 SKILL.md 缺失 | 記錄 `MISSING`，繼續 |
| stage 過濾（如 "s3 only"） | 只掃該 stage，其餘標記 `SKIPPED` |

### Step 1 — 載入評估基線

讀取 `references/skill-design-intent.md` 獲得檢查定義與基線。若缺失：BLOCKED。

### Step 2 — 三軌掃描

對每個 skill 執行三層檢驗：靜態句法冒煙（C1–C4）、ParanoidJudge 結構語意（J1–J2）、行為測試覆蓋率。
→ 各軌判定條件與綜合判定表：`references/s0-eval-alignment-checks.md`

### Step 3 — 產生批次報告

寫入 `docs/skill-evals/YYYY-MM-DD-alignment-scan.md`：總覽表、漂移清單、優先修復建議（≤ 5 條）。

### Step 4 — Commit & Report

`git add docs/skill-evals/ && git commit -m "eval: alignment scan $(date +%Y-%m-%d)"`

呈現報告路徑與摘要，等待批准。

## Completion Report

- **DONE** — 全部 skill 掃描完成，報告已提交。
- **DONE_WITH_CONCERNS** — 掃描完成，但 ≥1 個 skill 為 MISSING；已記錄在報告中。
- **BLOCKED** — `skills/` 目錄不存在或 `references/skill-design-intent.md` 缺失。
- **NEEDS_CONTEXT** — 用戶提供的 stage 過濾無法匹配任何 skill。

</what-to-do>

<supporting-info>
**Reads**: skills/s*/SKILL.md、references/skill-design-intent.md
**Writes**: docs/skill-evals/YYYY-MM-DD-alignment-scan.md
→ Full reference: `references/detail.md`
</supporting-info>
