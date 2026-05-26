---
name: s0-grill-docs
description: >
  Use when CONTEXT.md exists but the codebase has evolved — cross-references code
  terminology against CONTEXT.md, surfaces drift, updates inline. Evolution-phase
  tool. NOT for projects without CONTEXT.md (use /s1-config-context instead).
---

<HARD-GATE>
Do NOT update CONTEXT.md until the user has approved each proposed change.

⛔ OUTPUT DISCIPLINE:
After presenting all proposed changes, await explicit approval before writing.
Do NOT auto-invoke any pipeline skill.
</HARD-GATE>

<what-to-do>

**Terminology Auditor**: Your job is to find gaps between what the codebase actually says and what CONTEXT.md defines. Code is the source of truth for what terms are *in use*; CONTEXT.md is the source of truth for what they *mean*. Drift between the two creates AI hallucination.

### 絕對不要觸發的情境

| 情境 | 改用 |
|------|------|
| 專案沒有 CONTEXT.md | `/s1-config-context` — 先建立術語表；此 skill 需要已存在的 CONTEXT.md 作為基線 |
| 你想從頭定義 AI 邊界或 Agent 權限 | `/s1-config-context` — 邊界定義是建立期工作，非演進期審計 |
| 你想修改 lint 規則或架構約束 | `/s1-define-rules` — 規範管理；與術語無關 |

### Step 0 — Input Validation

| 失敗情境 | 行為 |
|---------|------|
| `CONTEXT.md` 不存在 | 停止：「此 skill 需要已存在的 CONTEXT.md。請先執行 `/s1-config-context`。」|
| 用戶未指定目標路徑 | 默認掃描 `src/` 或 `app/` 目錄；若兩者皆不存在，詢問用戶提供路徑 |

### Step 1 — Baseline Read

1. 讀取 `CONTEXT.md` — 提取所有已定義術語
2. 建立基線術語表（term → definition）

### Step 2 — Code Terminology Extraction

掃描目標代碼文件。對每個文件提取：
- **類名、函數名、變量名**中看起來像領域概念的詞（排除基礎設施術語如 `config`、`util`、`logger`）
- **字串字面量**中看起來像領域實體名稱的詞
- **注釋**中定義或描述領域概念的表述

產出：代碼中的候選術語原始清單（含文件路徑和行號）。

### Step 3 — Drift Analysis

比對代碼術語與 CONTEXT.md 基線：

| 分類 | 定義 | 行動 |
|------|------|------|
| **Aligned** | 術語存在於 CONTEXT.md，且代碼用法符合定義 | 無需行動 |
| **Undocumented** | 術語存在於代碼，但**不在** CONTEXT.md | 提案新增 |
| **Contradicted** | 術語在兩者皆有，但代碼用法與 CONTEXT.md 定義**衝突** | 提案挑戰 |
| **Stale** | 術語在 CONTEXT.md 但**不存在**任何代碼文件 | 標記供審查（可能是刻意的） |

### Step 4 — Challenge Loop

對每個 Undocumented 或 Contradicted 術語，逐一處理：

**Undocumented 術語：**
1. 展示：「在 `[file:line]` 發現 `[term]` — 不在 CONTEXT.md 中。根據用法，它似乎表示：[從代碼推斷的含義]。這正確嗎？」
2. 等待用戶回應
3. 確認 → 標記 `[TO ADD]`
4. 糾正 → 記錄用戶提供的定義，標記 `[TO ADD - user-corrected]`
5. 拒絕 → 標記 `[SKIP]`

**Contradicted 術語：**
1. 展示：「CONTEXT.md 將 `[term]` 定義為『[definition]』，但在 `[file:line]` 中它似乎表示『[code usage]』。哪個正確？」
2. 等待決策；標記 `[UPDATE CONTEXT]` 或 `[CODE SMELL — review code]`

一次一個。不批量處理。

### Step 5 — Write Updates

呈現 CONTEXT.md 提案修改的完整 diff。等待明確批准。然後原地更新 CONTEXT.md。

**更新規則：**
- 只更新 `## Language` 區段（術語定義）
- 不觸碰 `## AI Boundaries` 或 `## Architecture` 區段（這些是建立期設定）
- 新增術語按字母排序插入

## Completion Report

- **DONE** — 漂移分析完成；CONTEXT.md 已更新批准的變更；stale 術語已標記。
- **DONE_WITH_CONCERNS** — 已更新，但列出：未移除的 stale 術語、透過更新代碼（非 CONTEXT.md）解決的衝突、或大量未記錄的術語表面。
- **BLOCKED** — 用戶無法釐清某個衝突術語；陳述哪個術語及所需資訊。
- **NEEDS_CONTEXT** — 目標代碼路徑不存在或無法讀取；陳述缺少什麼。

</what-to-do>

<supporting-info>

**演進期工具**：在代碼成長超過 CONTEXT.md 文件記錄時使用。對比 `/s1-config-context`（建立期：無代碼存在，從頭定義，必須先問後寫規則）。

| Skill | 使用時機 | 前置條件 |
|-------|---------|---------|
| `s1-config-context` | 建立期：CONTEXT.md 不存在 | 無（從頭開始） |
| `s0-grill-docs` | 演進期：CONTEXT.md 已存在但代碼已成長 | CONTEXT.md 必須已存在 |

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-grill-docs/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: `CONTEXT.md`、目標代碼文件（默認 `src/` 或 `app/`）
- **Writes**: `CONTEXT.md`（僅原地更新）

</supporting-info>
