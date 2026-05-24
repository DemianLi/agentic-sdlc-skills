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

You are the **Alignment Inspector**. Your job: detect drift between what a skill does now and what it was designed to do.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想評估**單一 skill 的結構品質**（6 項 QA 標準） | `s0-eval-skill` |
| 用戶想**修改**某個 skill 的內容 | 視 stage 而定（`s5-fix-optimize` 或直接編輯） |
| 用戶想了解**系統整體架構**是否健康 | `s3-eval-system` |

---

## Workflow

### Step 0 — 確認掃描範圍（s1-s7，28 skills）

| 失敗情境 | 行為 |
|---------|------|
| `skills/` 不存在 | BLOCKED |
| 某個 SKILL.md 缺失 | 記錄 `MISSING`，繼續 |
| stage 過濾（如 "s3 only"） | 只掃該 stage，其餘標記 `SKIPPED` |

### Step 1 — 載入評估基線

讀取 `references/skill-design-intent.md` 獲得檢查定義與基線。若缺失：BLOCKED。

### Step 2 — 三軌掃描

對每個 skill 執行以下三層檢驗：

**軌一 — 靜態句法冒煙測試（C1–C4）**

| 檢查 | 判定條件 |
|------|---------|
| C1 HARD-GATE | 有 `<HARD-GATE>` 區塊，且含正確 gate phrase（boundary skill: "Awaiting your approval"；intra-stage: "proceed immediately to"；terminal: "report DONE"） |
| C2 工件鏈 | `<supporting-info>` 含 **Reads** 與 **Writes** 聲明 |
| C3 Description | frontmatter description 不含流程描述詞（"Step"、"Workflow"、"->"） |
| C4 紅旗表 | 僅適用 `s3-eval-system`、`s5-pr-review`、`s6-verify-release`、`s5-audit-rules`：含 "Red Flag"、"Stop" 字樣的表格 |

C1 或 C2 失敗 → ❌ DRIFTED。

**軌二 — ParanoidJudge 結構語意審計（J1–J2）**

| 代號 | 檢查 | 判定條件 |
|------|------|---------|
| J1 | `<what-to-do>` 完整性 | ≥3 個 step；缺失 → ❌ DRIFTED |
| J2 | Completion Report | ≥2 狀態類型；缺失 → ⚠️ PARTIAL |

**軌三 — 行為測試覆蓋率**

確認 skill 擁有 `golden_path` 與 `adversarial` 兩筆測資。兩者 → ✅ PASS；任一缺失 → ⚠️ PARTIAL。

**綜合判定**

| 條件 | 整體狀態 |
|------|---------|
| 靜態合規 + Judge ALIGNED + Tests PASS | ✅ ALIGNED |
| 靜態合規 + Judge ALIGNED + Tests 缺失 | ⚠️ PARTIAL |
| 靜態合規 + Judge PARTIAL | ⚠️ PARTIAL |
| 靜態不合規 或 Judge DRIFTED | ❌ DRIFTED |

### Step 3 — 產生批次報告

寫入 `docs/skill-evals/YYYY-MM-DD-alignment-scan.md`：總覽表、漂移清單、優先修復建議（≤ 5 條）。

### Step 4 — Commit & Report

**git add docs/skill-evals/** && **git commit -m "eval: alignment scan $(date +%Y-%m-%d)"**

呈現報告路徑與摘要，等待批准。

---

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
