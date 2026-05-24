---
name: s0-eval-skill
description: >
  Use when scoring any SKILL.md against 6 production-quality criteria. Outputs
  diagnostic report with defect coordinates. NOT for rewriting skills.
---

<HARD-GATE>
Do NOT edit or rewrite the evaluated skill file.
Do NOT auto-trigger any downstream skill.
The only permitted output is a structured evaluation report written to disk.

After presenting the report, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想*新建一個 Skill*（"幫我寫個 skill 做 X"） | `skill-creator` |
| 用戶想*改善程式碼品質*（lint、refactor、PR review） | `/s5-audit-rules` 或 `/s5-fix-optimize` |
| 用戶想*評估系統架構*或*技術債* | `/s3-eval-system` |
| 用戶已拿到評估結果、想*修改現有 Skill* | `/s5-fix-optimize` |

---

## Workflow

### Step 0 — Input Validation

接受唯一輸入：`skill_path`（SKILL.md 的絕對路徑）。

| 失敗情境 | 行為 |
|---------|------|
| 未提供路徑 | BLOCKED — 提問：「請提供 SKILL.md 的絕對路徑。」|
| 路徑不存在 | BLOCKED — 回報：「`<path>` 不存在，無法繼續。」 |
| 非 `.md` 副檔名 | BLOCKED — 回報：「預期 .md 檔，實際為 `<ext>`。」 |
| 檔案存在但無 YAML frontmatter | PARTIAL — 讀取全文；標準 3 記為 `❌ FAIL — frontmatter absent`，其餘繼續評分 |
| 檔案存在但缺 `<what-to-do>` | PARTIAL — 繼續；缺失 section 標記為 `❌ FAIL — section absent` |

### Step 1 — Read the Skill

讀取 `skill_path`。擷取：
- frontmatter 的 `name` 與 `description`
- 所有具名 section（`<HARD-GATE>`、`<what-to-do>`、`<supporting-info>`、所有 `###` header）
- 各 section 行數

若讀取失敗（權限錯誤、磁碟異常）→ BLOCKED — 「讀取失敗：[原因]，請確認路徑存在且有讀取權限。」

### Step 2 — Apply Scoring Rubric

載入 `references/scoring-rubric.md`（完整評分定義與判斷規則）。

若 rubric 檔案不存在 → BLOCKED — 「`references/scoring-rubric.md` 不存在，無法評分。請先建立該檔案。」

每個標準評分為：`✅ PASS` / `⚠️ PARTIAL` / `❌ FAIL`

| # | 標準 | 決定性檢查（精簡） |
|---|------|--------------------|
| 1 | 衝突防禦 | 正文是否點名 ≥1 個相鄰 skill 並說明差異？ |
| 2 | 雙向阻斷 | 是否有「絕對不要」區塊，含 ≥2 個具體反例？ |
| 3 | 輸入清洗 | 輸入是否明列，且每個失敗情境都有定義行為？ |
| 4 | 漸進披露 | 是否無單一 inline 區塊 > 50 行？大模板是否外部化？ |
| 5 | 優雅降級 | 每個可能失敗的步驟是否有 fallback 或失敗標籤？ |
| 6 | 漂移監控 | 是否引用 eval fixture 目錄，且 fixture 實際存在？ |

### Step 3 — Write Evaluation Report

若 `docs/skill-evals/` 不存在，自動建立該目錄後繼續；若建立失敗 → BLOCKED — 「無法建立目錄 `docs/skill-evals/`：[原因]。」

寫入：`docs/skill-evals/YYYY-MM-DD-<skill-name>-eval.md`

使用 `references/scoring-rubric.md` 中的報告模板。必填欄位：
- 每個標準的分數 + 行號證據
- 總分（X/6 PASS）
- 每個 ❌ 或 ⚠️ 的具體缺陷描述
- 建議下一步（一句話）

### Step 4 — Present and Wait

呈現檔案路徑與完整報告內容。**等待明確批准，不自動進入下一階段。**

---

## Completion Report

- **DONE** — 報告已寫入磁碟；全部 6 項已評分。
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
