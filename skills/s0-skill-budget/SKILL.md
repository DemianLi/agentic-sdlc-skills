---
name: s0-skill-budget
description: >
  Use when adding or modifying any SKILL.md — audits token efficiency (D/I/S axes).
  NOT for structural quality (s0-eval-skill) or drift detection (s0-eval-alignment).
---

<HARD-GATE>
Do NOT edit any skill file during this audit.
Do NOT auto-trigger any downstream skill.
Output: one compact checklist block in chat. No file written.

After presenting the report, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Token Budget Auditor**. Three checks. No edits. One output block.

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

### Step 1 — D 軸：Description Budget（方案 A 合規）

讀取 frontmatter 的 `description:` 欄位。若欄位缺失，D1–D5 全部 ❌ FAIL。

估計 token 數方法：字串長度 ÷ 4，取整數。

| 代號 | 檢查 | 標準 | 判定 |
|------|------|------|------|
| D1 | 長度 | 估計 token 數 ≤ 40 | ✅ / ❌ |
| D2 | 觸發詞 | 含 "Use when" 且後接任務類型關鍵字 | ✅ / ❌ |
| D3 | 輸出物 | 含 "Outputs:" 或具體輸出物名稱 | ✅ / ⚠️ |
| D4 | 排除子句 | 含 "NOT" 且後接具體排除場景 | ✅ / ❌ |
| D5 | 流程詞禁用 | 不含 "Step"、"->"、"Workflow" | ✅ / ❌ |

**優先級**：D1 + D2 任一 ❌ → 此 skill 在 deferred loading 中最難被精確命中，列為高優先缺陷。

---

### Step 2 — I 軸：Index Coverage（方案 C 合規）

讀取 `schemas/SKILL_INDEX.yaml`（路徑相對於 skill 所在 repo 根目錄）。

若 `SKILL_INDEX.yaml` 不存在：I1–I3 全部記為 `⚠️ N/A (index missing)`，並在 Issues 區塊加一行：
> `建議：建立 schemas/SKILL_INDEX.yaml，參考 references/SKILL_INDEX_TEMPLATE.yaml`

| 代號 | 檢查 | 標準 | 判定 |
|------|------|------|------|
| I1 | 已收錄 | skill name 出現為 index 的 value | ✅ / ❌ |
| I2 | 關鍵字覆蓋 | ≥ 2 個 keyword 指向此 skill | ✅ / ❌ |
| I3 | 互斥性 | 無 keyword 同時指向相鄰 stage 的其他 skill | ✅ / ⚠️ |

I3 判定方法：取此 skill 的所有 keyword，逐一檢查 index 中是否有其他 skill 也用了相同 keyword。有重疊 → ⚠️，列出衝突 keyword。

---

### Step 3 — S 軸：Size Budget

統計 skill_path 的位元組數與各 `###` section 行數。

| 代號 | 檢查 | 標準 | 判定 |
|------|------|------|------|
| S1 | 檔案大小 | ≤ 10 KB | ✅ / ❌ |
| S2 | 單 section 長度 | 無任何 `###` section 超過 50 行 | ✅ / ❌ |
| S3 | 外部引用存在 | `Reads:` 列出的所有檔案在 repo 中存在 | ✅ / ⚠️ |

S2 檢查方式：解析 `###` header 位置，計算每個 section 到下個 header（或檔案尾）的行數。

---

### Step 4 — 輸出報告

**不寫入磁碟**。直接在 chat 呈現以下格式（詳細模板見 `references/SKILL_INDEX_TEMPLATE.yaml` 末節）：

```
Token Budget Audit: <skill-name>  (<KB>, ~<tokens>)
D  D1[✅/❌] D2[✅/❌] D3[✅/⚠️] D4[✅/❌] D5[✅/❌]
I  I1[✅/❌] I2[✅/❌] I3[✅/⚠️]
S  S1[✅/❌] S2[✅/❌] S3[✅/⚠️]
Overall: PASS / PARTIAL / FAIL
Issues:
- [代號]: [缺陷] → [一句修改建議]  （無問題寫「— none —」）
```

Overall：全 ✅ → PASS；有 ⚠️ 無 ❌ → PARTIAL；有 ❌ → FAIL。

---

## Completion Report

- **PASS** — 全部 D/I/S 項均為 ✅；可合入。
- **PARTIAL** — 有 ⚠️ 但無 ❌；可合入，建議修正。
- **FAIL** — 有 ≥1 ❌；不建議合入，說明具體項目。
- **BLOCKED** — 輸入驗證失敗；說明確切原因。

</what-to-do>

<supporting-info>

## Role Identity: Token Budget Auditor
- **Mindset**: 會計師。只數字，不主張。揭露缺口，不提供解法。
- **Upstream Dependency**: 任何 SKILL.md 路徑（新增或修改後）。
- **Downstream Target**: 用戶確認後，自行修正 SKILL.md 或 SKILL_INDEX.yaml。

## Semantic Boundary

| Skill | 評估什麼 | 此 skill 的差異 |
|-------|---------|----------------|
| `s0-eval-skill` | 6 項生產就緒標準（結構、語意邊界、測資） | 此 skill 只看 **token 加載成本**（D/I/S 三軸） |
| `s0-eval-alignment` | 設計意圖對齊度（批次掃描 28 個 skill） | 此 skill 單檔、聚焦加載成本；不看設計意圖 |
| `skill-creator` | 創建新 skill | 此 skill 審計已有草稿；不創建、不修改 |

## 建議使用時機

| 情境 | 使用方式 |
|------|---------|
| **新增 skill** | 完成 SKILL.md 草稿後，merge 前執行一次 |
| **修改 skill 功能** | 改動 `<what-to-do>` 後立即執行，確認 S 軸未超標 |
| **修改 description** | 改動後執行，確認 D1–D5 全部通過 |
| **擴充 SKILL_INDEX.yaml** | 新增 keyword 後執行，確認 I3 互斥性 |

## 與 s0-eval-skill 的搭配順序

新 skill 上線流程建議：
1. 草稿完成 → `/s0-skill-budget`（token 效率關卡）
2. 通過後 → `/s0-eval-skill`（結構品質關卡）
3. 兩者都 PASS → 合入

修改現有 skill 流程建議：
1. 改動完成 → `/s0-skill-budget`（快速；僅看改動影響面）
2. 若 Overall = FAIL → 修正後重跑
3. 確認 PASS/PARTIAL → 視需求決定是否跑完整 `/s0-eval-skill`

## Artifact Dependencies
- **Reads**: `skill_path`（用戶提供）、`schemas/SKILL_INDEX.yaml`（可選）
- **Writes**: 無（僅 chat 輸出）

## Eval Fixtures

冒煙測試：以此 skill 對自身執行（`skills/s0-skill-budget/SKILL.md`）。
預期結果：Overall = PASS。若自評 FAIL，修正 SKILL.md，不修改評分標準。

</supporting-info>
