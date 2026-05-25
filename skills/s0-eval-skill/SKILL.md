---
name: s0-eval-skill
description: >
  Use when scoring any SKILL.md against 7 production-quality criteria (P1–P5).
  Outputs diagnostic report with defect coordinates. NOT for rewriting skills.
---

<HARD-GATE>
Do NOT edit or rewrite the evaluated skill file.
Do NOT auto-trigger any downstream skill.
The only permitted output is a structured evaluation report written to disk.

After presenting the report, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

**When NOT to use**: New skill → `skill-creator`; code quality → `s5-audit-rules`/`s5-fix-optimize`; architecture → `s3-eval-system`; modify → `s5-fix-optimize`.
→ Reference: `references/s0-eval-skill-workflow.md`

**Workflow**: Step 0 — Validate input (skill_path must be .md, exist, have frontmatter). Step 1 — Read skill structure. Step 2 — Score 7 criteria vs `references/scoring-rubric.md`: C1 衝突防禦 (P1+), C2 雙向阻斷 (P1−), C3 輸入清洗 (P2 input), C4 漸進披露 (P4), C5 優雅降級 (P2 degrade), C6 漂移監控 (P5), C7 有界執行 (P3). Each scores PASS/WEAK/FAIL. Step 3 — Write report to `docs/skill-evals/YYYY-MM-DD-<skill-name>-eval.md`. Step 4 — Present & wait for approval.

### Step 0 — Input Validation

接受唯一輸入：`skill_path`（SKILL.md 絕對路徑）。

| 失敗情境 | 行為 |
|---------|------|
| 未提供路徑 | BLOCKED — 「請提供 SKILL.md 的絕對路徑。」|
| 路徑不存在 | BLOCKED — 「`<path>` 不存在。」 |
| 非 `.md` 副檔名 | BLOCKED — 「預期 .md 檔，實際為 `<ext>`。」 |
| 無 YAML frontmatter | DONE_WITH_CONCERNS — C3 記為 `❌ FAIL — frontmatter absent`，其餘繼續 |
| 缺 `<what-to-do>` | DONE_WITH_CONCERNS — 缺失 section 標記為 `❌ FAIL — section absent` |

### Step 1 — Read the Skill

讀取 `skill_path`。擷取：frontmatter `name`/`description`、所有具名 section、各 section 行數。讀取失敗 → BLOCKED。

### Step 2 — Apply Scoring Rubric

載入 `references/scoring-rubric.md`（7 準則定義、P-ID 對映、PASS/WEAK/FAIL 條件、報告模板）。若缺失 → BLOCKED。
→ 評分標準快查：`references/scoring-rubric.md`

### Step 3 — Write Evaluation Report

若 `docs/skill-evals/` 不存在，自動建立。寫入 `docs/skill-evals/YYYY-MM-DD-<skill-name>-eval.md`（模板於 rubric 檔）。必填：每標準分數 + 行號證據 + 缺陷描述 + 建議下一步。

### Step 4 — Present and Wait

呈現檔案路徑與完整報告內容。**等待明確批准，不自動進入下一階段。**

## Completion Report

- **DONE** — 報告已寫入磁碟；全部 7 項已評分；整體等級 READY/NEAR-READY/DRAFT 已標註。
- **DONE_WITH_CONCERNS** — 報告已寫入；記錄任何評分依據模糊的標準。
- **BLOCKED** — 輸入驗證失敗；說明確切原因。
- **NEEDS_CONTEXT** — 檔案存在但完全無法解析；說明缺少什麼。

</what-to-do>

<supporting-info>

## Artifact Dependencies
- **Reads**: `skill_path` (user provided), `references/scoring-rubric.md`
- **Writes**: `docs/skill-evals/YYYY-MM-DD-<skill-name>-eval.md`

→ Full reference: `references/detail.md`

</supporting-info>
