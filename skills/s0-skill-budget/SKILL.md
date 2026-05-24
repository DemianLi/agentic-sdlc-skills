---
name: s0-skill-budget
description: >
  Use when auditing SKILL.md token budget — D/I/S audit. Outputs checklist. NOT for
  quality audit or design drift scan.
---

<HARD-GATE>
Do NOT edit any skill file during this audit.
Do NOT auto-trigger any downstream skill.
Output: one compact checklist block in chat. No file written.

After presenting the report, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想評估 skill 的生產就緒度（結構、測資） | `s0-eval-skill` |
| 用戶想批次掃描設計意圖漂移 | `s0-eval-alignment` |
| 用戶想創建全新的 skill | `skill-creator` |
| 用戶想修改 skill 內容 | 確認 audit 結果後自行編輯；此 skill 不動檔案 |

---

### Step 0 — Input Validation

接受唯一輸入：`skill_path`（SKILL.md 的絕對路徑）。

| 失敗情境 | 行為 |
|---------|------|
| 路徑未提供 | BLOCKED — 「請提供 SKILL.md 路徑。」|
| 路徑不存在 | BLOCKED — 「`<path>` 不存在，無法繼續。」|
| 非 .md 副檔名 | BLOCKED — 「預期 .md 檔，實際為 `<ext>`。」|
| 無 YAML frontmatter | PARTIAL — 繼續；D 軸所有項記為 ❌ FAIL |

---

### Step 1 — D-Axis: Description Budget

Read frontmatter `description` field; if missing D1–D5 all ❌ FAIL. Token estimate: length ÷ 4.

| Code | Check | Standard |
|------|-------|----------|
| D1 | Length | tokens ≤ 40 |
| D2 | Trigger | starts "Use when" + task keyword |
| D3 | Output | contains "Outputs:" or artifact name |
| D4 | Exclusion | contains "NOT" + scenario |
| D5 | No workflow words | no "Step" / "->" / "Workflow" |

### Step 2 — I-Axis: Index Coverage

Read `schemas/SKILL_INDEX.yaml`. If missing: I1–I3 all ⚠️ N/A.
| Code | Check | Standard |
|------|-------|----------|
| I1 | Listed | skill name in index values |
| I2 | Keywords | ≥ 2 keywords point to skill |
| I3 | No conflicts | no keyword shared with adjacent stages |

### Step 3 — S-Axis: Size Budget

Measure `skill_path` byte size and section line counts.
| Code | Check | Standard |
|------|-------|----------|
| S1 | File size | ≤ 10 KB |
| S2 | Section length | no `###` section > 50 lines |
| S3 | External refs | all `Reads:` files exist |

### Step 4 — Output Report

**No file written.** Output to chat:

```
Token Budget Audit: <skill-name>  (<KB>, ~<tokens>)
D  D1[✅/❌] D2[✅/❌] D3[✅/⚠️] D4[✅/❌] D5[✅/❌]
I  I1[✅/❌] I2[✅/❌] I3[✅/⚠️]
S  S1[✅/❌] S2[✅/❌] S3[✅/⚠️]
Overall: PASS / PARTIAL / FAIL
Issues: [list or none]
```

Overall: all ✅ → PASS; has ⚠️ no ❌ → PARTIAL; has ❌ → FAIL.

## Completion Report

- **PASS** — 全部 D/I/S 項均為 ✅；可合入。
- **PARTIAL** — 有 ⚠️ 但無 ❌；可合入，建議修正。
- **FAIL** — 有 ≥1 ❌；不建議合入，說明具體項目。
- **BLOCKED** — 輸入驗證失敗；說明確切原因。

</what-to-do>

<supporting-info>

**Reads**: `skill_path` (user-provided), `schemas/SKILL_INDEX.yaml` (optional)  
**Writes**: none (chat output only)

→ Full reference: `references/detail.md`

</supporting-info>
