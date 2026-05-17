---
name: s0-eval-alignment
description: >
  Use when you need to verify that s1-s7 skills have not drifted from their original
  design intent. Batch-scans all skills against QA.md stage mapping and four-repo
  benchmark patterns. Outputs ALIGNED / PARTIAL / DRIFTED per skill.
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

### Step 0 — 確認掃描範圍

預設掃描所有 `skills/s1-*/SKILL.md` 至 `skills/s7-*/SKILL.md`（共 28 個 skill）。

| 失敗情境 | 行為 |
|---------|------|
| `skills/` 目錄不存在 | BLOCKED — 回報路徑並停止 |
| 某個 skill 目錄無 SKILL.md | 記錄為 `MISSING`，繼續其餘掃描 |
| 用戶提供 stage 過濾（如 "s3 only"） | 只掃描對應 stage，其餘標記 `SKIPPED` |

### Step 1 — 載入評估基線

讀取 `references/skill-design-intent.md`。

擷取：
- 跨 skill 模式檢查定義（C1 / C2 / C3 / C4）
- 每個 skill 對應的 QA.md 步驟號與必現關鍵詞列表

若檔案不存在：BLOCKED — 提示「評估基線缺失，請確認 references/skill-design-intent.md 存在」。

### Step 2 — 逐一掃描

對每個 skill 執行以下四項檢查：

**QA 對齊（Q）**：計算 SKILL.md 全文中出現設計意圖表中關鍵詞的數量。
- ✅ ALIGNED：≥ 3 個
- ⚠️ PARTIAL：1–2 個
- ❌ DRIFTED：0 個

**C1 強制執行**：SKILL.md 是否有 `<HARD-GATE>` 且含 "Awaiting your approval"。

**C2 工件鏈**：`<supporting-info>` 是否有 **Reads** 與 **Writes** 聲明。

**C3 Description 格式**：frontmatter description 是否包含 "Step"、"Workflow"、"->" 等流程描述詞。

**C4 紅旗表**（僅 `s3-eval-system`、`s5-pr-review`、`s6-verify-release`、`s5-audit-rules`）：是否含 "Red Flag"、"Stop"、"Rationalization" 字樣的表格。

### Step 3 — 產生批次報告

寫入：`docs/skill-evals/YYYY-MM-DD-alignment-scan.md`

使用 `references/skill-design-intent.md` 中定義的報告模板格式（見該檔案末節）。必填欄位：
- 總覽表：每個 skill 的 Q / C1 / C2 / C3 / C4 狀態
- 漂移清單：所有 DRIFTED 或 PARTIAL 的 skill 及具體缺失關鍵詞
- 優先修復建議（≤ 5 條，按影響排序）

### Step 4 — Commit

```bash
git add docs/skill-evals/
git commit -m "eval: alignment scan $(date +%Y-%m-%d)"
```

### Step 5 — 呈現並等待

列出報告路徑與總覽表摘要，等待明確批准。

---

## Completion Report

- **DONE** — 全部 skill 掃描完成，報告已提交。
- **DONE_WITH_CONCERNS** — 掃描完成，但 ≥1 個 skill 為 MISSING；已記錄在報告中。
- **BLOCKED** — `skills/` 目錄不存在或 `references/skill-design-intent.md` 缺失。
- **NEEDS_CONTEXT** — 用戶提供的 stage 過濾無法匹配任何 skill。

</what-to-do>

<supporting-info>

## Role Identity: Alignment Inspector
- **Mindset**: 對照設計意圖，找出現實與設計的落差。不修改，只診斷。
- **Upstream Dependency**: `references/skill-design-intent.md`（評估基線）
- **Downstream Target**: 用戶確認後，由對應 stage 的維護者修復漂移 skill。

## Semantic Boundary

| Skill | 評估什麼 | 此 skill 的差異 |
|-------|---------|----------------|
| `s0-eval-skill` | 單一 skill 的 6 項結構品質 | 此 skill 評估**設計意圖對齊度**，批次跑完所有 28 個 skill |
| `s3-eval-system` | 軟體系統架構與爆炸半徑 | 此 skill 評估 skill 文件與原始需求的語意吻合度 |
| `s5-audit-rules` | 代碼對 RULES.md 的合規性 | 此 skill 不看代碼，只看 skill 文件 |

## Eval Fixtures

Fixtures 位於 `tests/fixtures/`；預期輸出位於 `tests/expected/`。

- `skill-aligned/SKILL.md` — 對齊案例（Q: ALIGNED, C1-C3: PASS）
- `skill-drifted/SKILL.md` — 漂移案例（Q: DRIFTED，關鍵詞全缺失）

冒煙測試：以此 skill 對 `tests/fixtures/` 中兩個 fixture 進行掃描，對照 `tests/expected/alignment-scan.md` 驗證輸出格式與判斷邏輯。

## Artifact Dependencies
- **Reads**: `skills/s*/SKILL.md`（全部）、`references/skill-design-intent.md`
- **Writes**: `docs/skill-evals/YYYY-MM-DD-alignment-scan.md`

</supporting-info>
