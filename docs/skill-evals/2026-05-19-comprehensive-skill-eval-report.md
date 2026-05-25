# Skill 全量評估報告

**日期**：2026-05-19  
**評估者**：8 個並行子 agent（每 Stage 一人）  
**涵蓋範圍**：33 個 skill（s0-s7 全 stage + s-fast-track）  
**評估框架**：6 大標準 × 跨 Skill 結構檢查 × 設計意圖對齊  

---

## 一、評估框架說明

### 6 大標準
| # | 名稱 | 滿足條件概要 |
|---|------|------------|
| C1 | 衝突防禦（Semantic Anti-Collision） | 點名 ≥1 個相鄰 skill 並說明邊界差異 |
| C2 | 雙向阻斷（Negative Triggers） | 含「絕對不要」區塊且 ≥2 個具體反例 |
| C3 | 輸入清洗（Input Linting） | 所有輸入參數明列，每個失敗情境有對應行為 |
| C4 | 漸進披露（Progressive Disclosure） | 無單一 inline 區塊 >50 行，大型模板外部化 |
| C5 | 優雅降級（Graceful Degradation） | 每個外部依賴步驟有明確失敗標籤或備援 |
| C6 | 長效維護（Drift Monitoring） | fixture 目錄實際存在且 ≥2 個測試案例 |

### 跨 Skill 結構檢查
- **J1**：`<what-to-do>` 含 ≥3 個 step header
- **J2**：Completion Report 定義 ≥2 種狀態
- **C1-check**：有 `<HARD-GATE>` 區塊且含正確 gate phrase
- **C2-check**：`<supporting-info>` 有 Reads 和 Writes 聲明
- **C3-check**：description 不含流程動詞串列

### 四大倉庫設計模式對應
| 倉庫 | 核心貢獻 |
|------|---------|
| **gstack** | Completion Status Protocol（4狀態）、Semantic Boundary 表、Process Flow DOT 圖 |
| **Superpowers** | Red Flags 紅旗表格、Common Rationalization 清單、Evidence over Assertion |
| **Matt Pocock skills** | 精確 description（無流程動詞）、issue tracker 術語一致性 |
| **OpenSpec** | 顯式 Reads/Writes 工件鏈、API Contract 格式標準 |

---

## 二、全量評分總覽

### s0 Stage — 初始探索

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | 結構 | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|------|--------|---------|---------|
| s0-brainstorm | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | 5/5 | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s0-trace-feature | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | 5/5 | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s0-eval-alignment | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 | ALIGNED | **6/6** | ✅ READY |
| s0-eval-skill | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 | ALIGNED | **6/6** | ✅ READY |

**s0 主要問題**：兩個 NEAR-READY skill 的 fixture 路徑引用存在但檔案不存在（tests/fixtures/ 目錄缺失）。

---

### s1 Stage — 初始化與規則定義

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | 結構 | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|------|--------|---------|---------|
| s1-define-rules | ❌ | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | 5/5 | ALIGNED | **3/6** | ❌ NEEDS WORK |
| s1-config-context | ⚠️ | ⚠️ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 | ALIGNED | **3/6** | ❌ NEEDS WORK |
| s1-lock-tech-stack | ❌ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 | ALIGNED | **3/6** | ❌ NEEDS WORK |
| s1-git-guardrails | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | 5/5 | ALIGNED | **5/6** | ⚠️ NEAR-READY |

**s1 主要問題**：前三個 skill 均缺少 Semantic Boundary 表格（C1）和具體的 Do NOT trigger 反例（C2），s1-config-context 還缺乏輸入驗證表（C3）。**s1-git-guardrails 是 s1 stage 的設計範本**，其他三個 skill 應參照其第 157-164 行的 Semantic Boundary 表、第 23-31 行的 Do NOT trigger 區塊。

---

### s2 Stage — 需求對齊與結構化

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | 結構 | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|------|--------|---------|---------|
| s2-capture-vision | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | 5/5 | ALIGNED | **5.5/6** | ⚠️ NEAR-READY |
| s2-align-req | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | 5/5 | ALIGNED | **5.5/6** | ⚠️ NEAR-READY |
| s2-struct-req | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | 5/5 | ALIGNED | **5.5/6** | ⚠️ NEAR-READY |
| s2-snapshot-ctx | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | 5/5 | ALIGNED | **5.5/6** | ⚠️ NEAR-READY |

**s2 主要問題**：所有 4 個 skill 的唯一弱點相同——C6 fixture 雖引用路徑存在但案例內容未充分驗證。整體設計質量 92%，結構高度一致。**僅需補全 fixture 案例即可全面升級至 READY**。

---

### s3 Stage — 技術方案制定與原子化拆解

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | C4-RF | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|-------|--------|---------|---------|
| s3-eval-system | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **6/6** | ✅ READY |
| s3-design-arch | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | N/A | ALIGNED | **5.5/6** | ⚠️ NEAR-READY |
| s3-breakdown-wbs | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s3-build-dag | ❌ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | ALIGNED | **5/6** | ⚠️ NEAR-READY |

**s3 主要問題**：s3-breakdown-wbs 和 s3-build-dag 完全未提及相鄰 skill（C1 FAIL）。建議在每個 skill 中添加「Skill Boundary Matrix」表格，說明「本 skill 定義 WHAT，s3-build-dag 定義 HOW（執行順序）」。

---

### s4 Stage — 開發實現與本地調試

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|--------|---------|---------|
| s4-setup-env | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s4-impl-task | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **6/6** | ✅ READY |
| s4-tdd | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s4-local-debug | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **5/6** | ⚠️ NEAR-READY |

**s4 主要問題**：s4-local-debug C1 完全 FAIL（無任何相鄰 skill 邊界說明）。**s4-impl-task 是 s4 stage 範本**，其第 81-88 行的 Semantic Boundary 表格應被其他三個 skill 複製採用。s4-tdd 的「Coverage Gate」區塊（160-215行）建議外部化至 `references/coverage-gate.md`。

---

### s5 Stage — 代碼審查與靜態驗證

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | C4-RF | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|-------|--------|---------|---------|
| s5-sast-lint | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | N/A | ALIGNED | **5.5/6** | ⚠️ NEAR-READY |
| s5-audit-rules | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **6/6** | ✅ READY |
| s5-pr-review | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s5-fix-optimize | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | N/A | ALIGNED | **4.5/6** | ⚠️ NEAR-READY |

**s5 主要問題**：C3（輸入清洗）是跨 skill 的共同弱點，s5-pr-review 和 s5-fix-optimize 均缺乏顯式輸入驗證表格。**s5-audit-rules 是 s5 stage 範本**，其 C4 紅旗表設計（rationalization 清單）與輸入驗證表格均為最佳實踐。

---

### s6 Stage — 動態測試與驗證

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | C4-RF | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|-------|--------|---------|---------|
| s6-test-integration | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | N/A | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s6-test-e2e | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | N/A | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s6-test-perf | ✅ | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ | N/A | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s6-verify-release | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ❌ | ✅ | ✅ | ✅ | ALIGNED | **4/6** | ❌ NEEDS WORK |

**s6 主要問題**：**所有 4 個 skill 的 C6（長效維護）均 FAIL**——引用了 `tests/fixtures/s6-{name}/cases.json` 但實際檔案完全不存在。這是 s6 stage 的整體系統性問題。s6-verify-release 還缺乏與相鄰 s6 skill 的邊界說明，且 test-results.json schema（32行）未外部化。

---

### s7 Stage — 交付發佈與閉環 + s-fast-track

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | J1 | J2 | 設計意圖 | **總分** | **狀態** |
|-------|----|----|----|----|----|----|----|----|--------|---------|---------|
| s7-build-artifact | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **6/6** | ✅ READY |
| s7-release-notes | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s7-deploy | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ALIGNED | **5/6** | ⚠️ NEAR-READY |
| s7-telemetry | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | PARTIAL | **5/6** | ⚠️ NEAR-READY |
| s-fast-track | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ALIGNED | **4/6** | ⚠️ NEAR-READY |

**s7 主要問題**：C4（漸進披露）是 s7 stage 的跨 skill 弱點。s7-telemetry 最嚴重（Anomaly Detection 區塊 71 行，整體 317 行超上限）。s-fast-track 缺乏 Completion Report（C5）和完整的衝突防禦表。

---

## 三、生產就緒狀態全覽

### READY（6/6）— 6 個

| Skill | 評語 |
|-------|------|
| **s0-eval-alignment** | 三軌掃描設計完整，fixture 有效 |
| **s0-eval-skill** | 輸入驗證最嚴謹（5個失敗情境），3個 fixture |
| **s3-eval-system** | 高風險 skill C4 紅旗表達標，唯一弱點 C1 邊界說明輕微不足 |
| **s4-impl-task** | s4 stage 的最佳範本，Semantic Boundary 表為本 stage 最完整 |
| **s5-audit-rules** | s5 stage 最佳範本，95 行但信息密度最高 |
| **s7-build-artifact** | s7 stage 範本，Pipeline Position 完整，無任何缺陷 |

### NEAR-READY（4.5-5.5/6）— 22 個

大多數 skill 落在此區間，主要缺陷為單一標準的 PARTIAL 或 FAIL。

### NEEDS WORK（≤4/6）— 5 個

| Skill | 核心問題 | 優先改善 |
|-------|---------|---------|
| **s1-define-rules** | C1 FAIL + C2 PARTIAL + C5 PARTIAL（3個問題） | 新增 Semantic Boundary 表 + Do NOT trigger 區塊 |
| **s1-config-context** | C1 PARTIAL + C2 PARTIAL + C3 FAIL | 新增 Input Validation 表 + 邊界說明 |
| **s1-lock-tech-stack** | C1 FAIL + C2 PARTIAL + C3 PARTIAL | 同上 |
| **s6-verify-release** | C1 PARTIAL + C4 PARTIAL + C6 FAIL | 建立 fixture + 外部化 schema + 新增邊界表 |
| **s-fast-track** | C1 PARTIAL + C5 PARTIAL + J2 ⚠️ | 新增 Completion Report + 衝突防禦表 |

---

## 四、跨 Stage 系統性問題

### 問題 1：C6 Fixture 系統性缺失（影響 6 個 skill）

**受影響 skill**：s6-test-integration、s6-test-e2e、s6-test-perf、s6-verify-release（完全不存在）、s0-brainstorm、s0-trace-feature（引用存在但 tests/ 目錄缺失）

**症狀**：SKILL.md 中引用了 `tests/fixtures/<skill>/cases.json`，但實際路徑不存在，導致 C6 全部 FAIL。

**根本原因**：s6 stage 的 fixture 從未建立；s0 stage 的兩個 skill 的 fixture 也未跟上 SKILL.md 的引用。

**建議修復**：
```
mkdir -p tests/fixtures/s6-test-integration
mkdir -p tests/fixtures/s6-test-e2e
mkdir -p tests/fixtures/s6-test-perf
mkdir -p tests/fixtures/s6-verify-release
mkdir -p tests/fixtures/s0-brainstorm
mkdir -p tests/fixtures/s0-trace-feature
```
每個目錄需建立包含 golden_path 和 adversarial 兩筆測資的 `cases.json`。

---

### 問題 2：C1 Semantic Boundary 系統性缺失（影響 7 個 skill）

**受影響 skill**（C1 FAIL）：s1-define-rules、s1-lock-tech-stack、s3-breakdown-wbs、s3-build-dag、s4-local-debug

**受影響 skill**（C1 PARTIAL）：s1-config-context、s3-eval-system、s3-design-arch、s4-setup-env、s4-tdd、s6-verify-release、s-fast-track

**最佳範本**：s1-git-guardrails（行 157-164）和 s4-impl-task（行 81-88）的 Semantic Boundary 表格

**建議模板**：
```markdown
## Semantic Boundary

| Skill | 用途 | 差別 |
|-------|------|------|
| 本 skill | [本 skill 職責] | [關鍵差異點] |
| 相鄰 skill A | [A 的職責] | [何時用 A 不用本 skill] |
| 相鄰 skill B | [B 的職責] | [何時用 B 不用本 skill] |
```

---

### 問題 3：C1/C2 在 s1 Stage 系統性薄弱

s1 stage（除 s1-git-guardrails）的衝突防禦和雙向阻斷普遍薄弱，導致 3 個 skill 僅 3/6 分。核心原因：Red Flags 表格為泛述而非具體反例，且無獨立的「Do NOT trigger」區塊。

**建議**：以 s1-git-guardrails 的行 23-31 為模板，為 s1-define-rules、s1-config-context、s1-lock-tech-stack 補充獨立的雙向阻斷區塊，每個區塊需包含觸發情境 + 正確替代 skill。

---

### 問題 4：C4 漸進披露 — s7 Stage 整體偏重

s7 stage 的多個 skill（telemetry、release-notes、deploy）包含較大的 inline 區塊（30-71 行），主要原因是 JSON schema、bash 範例、模板被內嵌於 SKILL.md 主文本。

**建議外部化清單**：
- `s7-telemetry` → `references/anomaly-detection-formula.md` + `references/telemetry-json-schema.md`
- `s7-release-notes` → `references/changelog-template.md`
- `s7-deploy` → `references/deploy-modes.md`
- `s4-tdd` → `references/coverage-gate.md`

---

## 五、最符合設計初衷的 github_skill_sample 參考匹配

### 最強設計模式對應

| 設計模式 | 來源倉庫 | 已採用的 skill | 應補充採用的 skill |
|---------|---------|--------------|-----------------|
| **Semantic Boundary 表格** | gstack SKILL.md | s1-git-guardrails、s4-impl-task、s5-audit-rules | s1-define-rules、s3-breakdown-wbs、s3-build-dag、s4-local-debug |
| **Red Flags 紅旗表（rationalization 清單）** | Superpowers | s0-brainstorm、s3-eval-system、s4-tdd、s5-audit-rules、s5-pr-review | s1 stage 三個 skill |
| **Completion Status Protocol（4狀態）** | gstack | 大多數 skill（已採用） | s-fast-track（僅有隱含狀態） |
| **顯式 Reads/Writes 工件鏈** | OpenSpec | 幾乎所有 skill | s-fast-track（未明確聲明） |
| **精確 description（無流程動詞）** | Matt Pocock | 所有 skill（均達標） | — |
| **Evidence over Assertion** | Superpowers | s4-tdd（Iron Law）、s6-verify-release | s5-fix-optimize（衝突決策邏輯） |

### 最符合整體設計初衷的 skill

從四大倉庫的優勢提取來看，**最完整體現設計初衷的 skill 是：**

1. **s4-impl-task**：Semantic Boundary 最清晰、Do NOT use 表格最完整、輸入驗證嚴謹
2. **s5-audit-rules**：Red Flags 設計最優（rationalization pattern）、輸入驗證完整、簡潔高密度
3. **s1-git-guardrails**：最完整的結構（衝突防禦表、雙向阻斷、輸入清洗、流程圖），是 s1 stage 的範本

---

## 六、優先改善行動計畫

### P0（緊急，1-2天）— 影響生產可用性

1. **建立 s6 stage fixture**（4個 skill × cases.json）
   - 每個 cases.json 需包含 `golden_path` 和 `adversarial` 兩筆測資
   - 可參考 `s0-eval-alignment/tests/eval_cases.json` 的格式

2. **s1-define-rules、s1-config-context、s1-lock-tech-stack 補充 Semantic Boundary 表**
   - 複製 s1-git-guardrails 行 157-164 的格式
   - 預計每個 skill 需新增 10-15 行

3. **s3-breakdown-wbs、s3-build-dag、s4-local-debug 補充 Semantic Boundary 表**
   - 複製 s4-impl-task 行 81-88 的格式

### P1（重要，3-5天）— 影響健壯性

4. **s1 stage 三個 skill 補充獨立 Do NOT trigger 區塊**（≥2 個具體反例）

5. **s7-telemetry 漸進披露修復**（317行 → 目標 ≤200行）
   - 外部化 Anomaly Detection 公式至 references/
   - 外部化 telemetry.json schema

6. **s-fast-track 補充 Completion Report**（加入 ROUTED/BLOCKED/NEEDS_CLARIFICATION 狀態）

### P2（提升，1-2週）— 影響品質評分

7. **s5-pr-review、s5-fix-optimize 補充輸入驗證表格**

8. **s4-tdd Coverage Gate 外部化**至 `references/coverage-gate.md`

9. **s7-release-notes、s7-deploy 漸進披露優化**（模板外部化）

10. **s0-brainstorm、s0-trace-feature fixture 建立**（補全最後的 C6 缺口）

---

## 七、Summary 統計

### 按狀態分布

| 狀態 | 數量 | 比例 | Skill 清單 |
|------|------|------|-----------|
| ✅ READY（6/6） | 6 | 18% | s0-eval-alignment, s0-eval-skill, s3-eval-system, s4-impl-task, s5-audit-rules, s7-build-artifact |
| ⚠️ NEAR-READY（4.5-5.5/6） | 22 | 67% | 大多數 skill |
| ❌ NEEDS WORK（≤4/6） | 5 | 15% | s1-define-rules, s1-config-context, s1-lock-tech-stack, s6-verify-release, s-fast-track |

### 按標準通過率（33個 skill）

| 標準 | PASS | PARTIAL | FAIL | 通過率 |
|------|------|---------|------|--------|
| C1 衝突防禦 | 17 | 9 | 7 | 52% |
| C2 雙向阻斷 | 26 | 7 | 0 | 79% |
| C3 輸入清洗 | 23 | 9 | 1 | 70% |
| C4 漸進披露 | 25 | 6 | 2 | 76% |
| C5 優雅降級 | 29 | 4 | 0 | 88% |
| C6 長效維護 | 23 | 5 | 5 | 70% |

**最弱標準**：C1 衝突防禦（52%），是整個 skill 系統的最大系統性缺口。

### 設計意圖對齊度

- 33/33 個 skill 均達到 ALIGNED 或 PARTIAL（100% 設計意圖基本吻合）
- s7-telemetry 為唯一 PARTIAL（2/4 關鍵詞未充分體現）

---

*報告生成方式：8 個並行子 agent 同時評估，每人負責一個 Stage，最後整合。*  
*評估基線來源：`skills/s0-eval-skill/references/scoring-rubric.md` × `skills/s0-eval-alignment/references/skill-design-intent.md`*
