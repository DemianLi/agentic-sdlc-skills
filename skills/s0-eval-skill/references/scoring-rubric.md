# Scoring Rubric — s0-eval-skill

每個標準的詳細判斷規則、PASS/PARTIAL/FAIL 邊界，以及輸出報告模板。

---

## Criterion 1 — 衝突防禦（Semantic Anti-Collision）

**目標**：確保同一系統中數十個 Skill 共存時，AI 不發生路由混淆。

| 分數 | 判斷條件 |
|------|---------|
| ✅ PASS | 正文含一個表格或段落，點名 ≥1 個相鄰 skill 的名稱（如 `/s3-eval-system`），並以「Distinct from」、「不同於」、「差異在於」等語言說明邊界 |
| ⚠️ PARTIAL | 提及相鄰 skill 但未說明差異；或說明模糊（如「類似但不同」） |
| ❌ FAIL | 正文完全未提及任何相鄰 skill |

**檢查位置**：`<supporting-info>` 的 "Semantic Boundary" 區塊，或 `<what-to-do>` 開頭的定位說明。

---

## Criterion 2 — 雙向阻斷（Negative Triggers）

**目標**：鎖死 AI 的過度泛化，防止錯誤路由。

| 分數 | 判斷條件 |
|------|---------|
| ✅ PASS | 含獨立區塊（header 含「絕對不要」、「Never」、「Do NOT trigger」等），且有 ≥2 列具體反例（每列須含：觸發情境 + 正確替代） |
| ⚠️ PARTIAL | 有負面觸發語言但 < 2 個具體反例；或反例過於泛化（如「不適用於所有程式碼問題」） |
| ❌ FAIL | 無任何負面觸發區塊 |

**檢查位置**：`<what-to-do>` 最頂端（路由階段即可讀到）。

---

## Criterion 3 — 輸入清洗（Input Linting / Schema Enforcement）

**目標**：防止雜訊輸入導致執行崩潰。

| 分數 | 判斷條件 |
|------|---------|
| ✅ PASS | 所有接受的輸入參數明列；每個失敗情境（缺少、型別錯誤、不存在）有對應的明確行為（BLOCKED / PARTIAL / 繼續） |
| ⚠️ PARTIAL | 輸入有列但失敗行為隱含（如「如果找不到就回報」）；或只覆蓋部分失敗情境 |
| ❌ FAIL | 無輸入定義；或接受任意輸入而未驗證 |

**加分條件**：前置 YAML frontmatter 有清楚的 `description`（說明 skill 接受什麼輸入）。

---

## Criterion 4 — 漸進披露（Progressive Disclosure）

**目標**：路由階段 AI 只讀精簡大綱，大型模板不塞入 SKILL.md。

| 分數 | 判斷條件 |
|------|---------|
| ✅ PASS | SKILL.md 中無單一連續 inline 區塊超過 50 行；大型模板、範本或歷史日誌以 `references/<file>` 形式外部化並明確引用 |
| ⚠️ PARTIAL | 有 51–100 行的單一區塊，但整體 SKILL.md < 150 行，仍算可接受 |
| ❌ FAIL | 任一單一區塊 > 100 行；或 SKILL.md 總行數 > 300 行且無外部引用 |

**量化方法**：計算 SKILL.md 內各 fenced code block 與連續段落的行數。

---

## Criterion 5 — 優雅降級（Fallback & Graceful Degradation）

**目標**：核心步驟失敗時系統仍能返回安全保底結果。

| 分數 | 判斷條件 |
|------|---------|
| ✅ PASS | 每個可能因外部因素失敗的步驟（網路請求、檔案讀寫、git commit、API 呼叫）都有明確的失敗標籤（BLOCKED / NEEDS_CONTEXT / DONE_WITH_CONCERNS）或備援行動 |
| ⚠️ PARTIAL | 部分步驟有 fallback，但至少一個外部依賴步驟無任何失敗定義 |
| ❌ FAIL | 所有步驟假設成功；無任何失敗情境定義 |

**參考**：Completion Report 區塊（BLOCKED / NEEDS_CONTEXT 狀態的存在是必要但不充分條件）。

---

## Criterion 6 — 長效維護（Drift Monitoring & Offline Evals）

**目標**：應對底層模型升級帶來的 Skill Drift；禁止 AI 在運行時修改 Playbook。

| 分數 | 判斷條件 |
|------|---------|
| ✅ PASS | 正文引用 fixture 目錄路徑，且該路徑下實際存在 ≥2 個 fixture 檔案（一 PASS、一 FAIL 案例）；或附有離線評估說明文件 |
| ⚠️ PARTIAL | 提及 fixture 或 eval set 但實際檔案不存在；或只有 1 個 fixture |
| ❌ FAIL | 無 fixture、無測試集、無離線評估任何提及 |

**自指禁令**：SKILL.md 不得包含允許 AI 在執行時覆寫自身的指令。

---

## 報告模板

寫入 `docs/skill-evals/YYYY-MM-DD-<skill-name>-eval.md` 時使用以下格式：

```markdown
## Skill Evaluation Report
**Skill**: `<name>`
**File**: `<absolute-path>`
**Date**: YYYY-MM-DD
**Evaluator**: s0-eval-skill

| # | 標準 | 分數 | 證據 |
|---|------|------|------|
| 1 | 衝突防禦 | ✅/⚠️/❌ | 行 N：「...」 |
| 2 | 雙向阻斷 | ✅/⚠️/❌ | 行 N：「...」 |
| 3 | 輸入清洗 | ✅/⚠️/❌ | 行 N：「...」 |
| 4 | 漸進披露 | ✅/⚠️/❌ | 最大 inline 區塊：N 行 |
| 5 | 優雅降級 | ✅/⚠️/❌ | 行 N：「...」 |
| 6 | 長效維護 | ✅/⚠️/❌ | fixture 路徑：存在/不存在 |

**總分**：X/6 PASS

### 缺陷清單
- ❌ 標準 N：<具體行號與問題描述>
- ⚠️ 標準 N：<具體行號與模糊點>

### 建議下一步
<一句話，例如：「補充 Criterion 2 的負面觸發區塊後可達 6/6。」>
```
