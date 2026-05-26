# Agentic SDLC Pipeline — Skill 使用場景地圖

**日期**：2026-05-26  
**範圍**：36 個 Skill 在 6 種開發情境下的推薦使用順序  
**依據**：`schemas/skill_graph_schema.yaml` + 各 Skill 的 SKILL.md 分析

---

## 情境 1：空泛的需求 + 無代碼庫

**適用場景**：用戶提出「我想做一個 X 應用」，沒有既有代碼，需求很模糊

| # | Skill | 性質 | 說明 |
|---|-------|------|------|
| 1 | **s0-grill** | ✅必做 | 深度訪談，梳理問題、痛點、方向，輸出決策樹 |
| 2 | **s1-config-context** | ✅必做 | 建立 CONTEXT.md，定義領域術語和 AI 邊界 |
| 3 | **s1-define-rules** | ✅必做 | 定義編碼標準，產出 RULES.md |
| 4 | **s1-lock-tech-stack** | ✅必做 | 鎖定技術棧，驗證相容性 |
| 5 | **s2-capture-vision** | ✅必做 | 轉化為 vision.md（problem/scope/approaches）|
| 6 | **s2-align-req** | ✅必做 | 解決 vision 中的歧義與邊界衝突 |
| 7 | **s2-struct-req** | ✅必做 | 結構化為可測試的 requirements.md（含 AC）|
| 8 | **s2-snapshot-ctx** | ✅必做 | 凍結需求為 CONTEXT_SNAPSHOT.md |
| 9 | **s3-eval-system** | ✅必做 | 評估變更衝擊範圍 |
| 10 | **s3-design-arch** | ✅必做 | 設計架構（OpenSpec 7 節：data/API/diagrams）|
| 11 | **s3-breakdown-wbs** | ✅必做 | 分解為原子任務（≤2-3 files，含 AC）|
| 12 | **s3-build-dag** | ✅必做 | 構建 TASK_DAG.md，識別平行機會 |
| 13 | **s4-setup-env** | ✅必做 | 準備環境、建立 feature branch |
| 14 | **s4-tdd** | ✅必做 | 先寫測試（紅燈） |
| 15 | **s4-impl-task** | ✅必做 | 實現代碼（綠燈） |
| 16 | **s4-local-debug** | ⚡可選 | 有 build failure / regression 才觸發 |
| 17 | **s5-sast-lint** | ✅必做 | Lint + SAST，阻止 CRITICAL findings |
| 18 | **s5-audit-rules** | ✅必做 | 規則合規審計 |
| 19 | **s5-pr-review** | ✅必做 | Code review |
| 20 | **s5-fix-optimize** | ✅必做 | 修復 CRITICAL/WARNING |
| 21 | **s6-test-integration** | ✅必做 | 集成測試 |
| 22 | **s6-test-e2e** | ✅必做 | E2E 測試 |
| 23 | **s6-test-perf** | ✅必做 | 性能基準（P99）|
| 24 | **s6-verify-release** | ✅必做 | 驗證所有測試通過 |
| 25 | **s7-build-artifact** | ✅必做 | 編譯/打包 |
| 26 | **s7-release-notes** | ✅必做 | 產出 CHANGELOG.md |
| 27 | **s7-deploy** | ✅必做 | 部署 |
| 28 | **s7-telemetry** | ✅必做 | 監控上線後指標 |

**跳過**：s0-grill-docs（無既有 CONTEXT.md）、s-fast-track（全新項目不適用快速路由）

---

## 情境 2：空泛的需求 + 腳手架

**適用場景**：代碼骨架已存在（如 Next.js starter），但產品需求未定義

**關鍵差異**：開頭先用 s0-grill-docs 稽核現有代碼與文檔同步；Stage 1 多項可選。

| # | Skill | 性質 | 說明 |
|---|-------|------|------|
| 1 | **s0-grill-docs** | ✅必做 | 掃描代碼與 CONTEXT.md 的術語漂移，更新術語表 |
| 2 | **s0-grill** | ✅必做 | 對模糊需求深度訪談，轉化為具體方向 |
| 3 | **s1-config-context** | ⚡可選 | CONTEXT.md 過時或不完整才執行 |
| 4 | **s1-define-rules** | ⚡可選 | RULES.md 不符現有代碼風格才更新 |
| 5 | **s1-lock-tech-stack** | ⚡可選 | 版本未鎖定才執行 |
| 6 | **s2-capture-vision** | ✅必做 | 從澄清的需求轉化為 vision spec |
| 7 | **s2-align-req** | ✅必做 | 解決 vision 中的歧義與邊界衝突 |
| 8 | **s2-struct-req** | ✅必做 | 結構化需求為可測試的 requirements.md |
| 9 | **s2-snapshot-ctx** | ✅必做 | 凍結快照 |
| 10 | **s3-eval-system** | ✅必做 | 評估新需求對既有代碼的衝擊 |
| 11 | **s3-design-arch** | ✅必做 | 設計新功能架構，含與現有架構的整合方案 |
| 12 | **s3-breakdown-wbs** | ✅必做 | 分解任務，標記哪些涉及現有代碼修改 |
| 13 | **s3-build-dag** | ✅必做 | 構建 DAG（考慮現有依賴）|
| 14–28 | **s4 → s7** | ✅必做 | 同情境 1 的 s4–s7 全段 |

---

## 情境 3：清晰的需求 + 腳手架

**適用場景**：PRD/spec 已定義，代碼骨架存在，直接開發

**跳過**：完整 Stage 1（文檔已存在）、s2-capture-vision（PRD 已定義）

| # | Skill | 性質 | 說明 |
|---|-------|------|------|
| 1 | **s0-grill-docs** | ⚡可選 | 最近有代碼變更時，快速確認術語一致性 |
| 2 | **s2-align-req** | ✅必做 | 驗證 PRD 完整性，解決歧義（邊界清晰才能進入實現）|
| 3 | **s2-struct-req** | ✅必做 | 確保每個 requirement 有可測試 AC |
| 4 | **s2-snapshot-ctx** | ✅必做 | 凍結快照 |
| 5 | **s3-eval-system** | ✅必做 | 評估變更衝擊 |
| 6 | **s3-design-arch** | ✅必做 | 設計架構（可能已有概要，細化之）|
| 7 | **s3-breakdown-wbs** | ✅必做 | 分解為原子任務 |
| 8 | **s3-build-dag** | ✅必做 | 構建 DAG |
| 9–24 | **s4 → s7** | ✅必做 | 同情境 1 |

---

## 情境 4：已有代碼庫 + 清晰需求 + 不熟悉架構

**適用場景**：現有代碼庫（如 legacy app），新增功能 PRD 清晰，但開發者不熟悉架構

**關鍵差異**：開頭雙 s0 理解 legacy；s3-design-arch 採用 `refactor-existing` mode。

| # | Skill | 性質 | 說明 |
|---|-------|------|------|
| 1 | **s0-grill** | ✅必做 | 訪談了解 legacy 代碼的歷史約束和設計原因 |
| 2 | **s0-grill-docs** | ✅必做 | 更新 CONTEXT.md，確保 AI 對術語理解與代碼一致 |
| 3 | **s2-align-req** | ✅必做 | 驗證新需求邊界（特別注意與現有功能的衝突）|
| 4 | **s2-struct-req** | ✅必做 | 結構化新需求 |
| 5 | **s2-snapshot-ctx** | ✅必做 | 凍結快照 |
| 6 | **s3-eval-system** | ✅必做 | 評估哪些 legacy files 受影響（最關鍵步驟）|
| 7 | **s3-design-arch** | ✅必做 | Mode: `refactor-existing`，明確整合點與技術債 |
| 8 | **s3-breakdown-wbs** | ✅必做 | 標記哪些任務涉及 legacy 代碼修改 |
| 9 | **s3-build-dag** | ✅必做 | legacy cleanup 優先排序 |
| 10–24 | **s4 → s7** | ✅必做 | 同情境 1（s4-tdd 需包含 legacy 迴歸測試）|

**跳過**：Stage 1（已有 RULES.md、CONTEXT.md、tech-stack）、s2-capture-vision（PRD 已定義）

---

## 情境 5：已有代碼庫 + 清晰需求 + 熟悉架構

**適用場景**：開發者熟悉現有代碼庫，PRD 清晰，快速開發新功能（brownfield + clear spec）

**最精簡路徑**：直接用 `s-fast-track` 路由到 Stage 4（27 skills → 16 skills）

| # | Skill | 性質 | 說明 |
|---|-------|------|------|
| 1 | **s-fast-track** | ✅必做 | 快速路由：確認 RULES.md 存在 → Standard Mode → 直接進 s4 |
| 2 | **s4-setup-env** | ✅必做 | 建立 feature branch |
| 3 | **s4-tdd** | ✅必做 | 寫測試 |
| 4 | **s4-impl-task** | ✅必做 | 實現 |
| 5 | **s4-local-debug** | ⚡可選 | 有 failure 才觸發 |
| 6 | **s5-sast-lint** | ✅必做 | Lint + SAST |
| 7 | **s5-audit-rules** | ✅必做 | 規則合規審計 |
| 8 | **s5-pr-review** | ✅必做 | Code review |
| 9 | **s5-fix-optimize** | ✅必做 | 修復 findings |
| 10 | **s6-test-integration** | ✅必做 | 集成測試 |
| 11 | **s6-test-e2e** | ✅必做 | E2E 測試 |
| 12 | **s6-test-perf** | ✅必做 | 性能基準 |
| 13 | **s6-verify-release** | ✅必做 | 驗證通過 |
| 14 | **s7-build-artifact** | ✅必做 | 編譯 |
| 15 | **s7-release-notes** | ✅必做 | CHANGELOG |
| 16 | **s7-deploy** | ✅必做 | 部署 |
| 17 | **s7-telemetry** | ✅必做 | 監控 |

**跳過**：Stage 0 grilling、Stage 1、Stage 2、Stage 3 全段

---

## 情境 6：解決用戶反饋的 Bug

**適用場景**：生產環境中發現 bug，需要快速修復

**Hotfix Mode**：`s-fast-track --hotfix` 路由，最短 11 個 skills

| # | Skill | 性質 | 說明 |
|---|-------|------|------|
| 1 | **s-fast-track** | ✅必做 | Hotfix Mode：輸入「用戶 X 在 Y 功能遇到 Z 錯誤」|
| 2 | **s4-setup-env** | ✅必做 | 檢出對應 commit，驗證環境 |
| 3 | **s4-local-debug** | ✅必做 | **優先**：重現 → 診斷根因 → 驗證修復（Hotfix 的核心）|
| 4 | **s4-impl-task** | ✅必做 | 最小化修復（不重構）|
| 5 | **s4-tdd** | ⚡可選 | 建議補迴歸測試，但 Hotfix 可豁免 |
| 6 | **s5-sast-lint** | ✅必做 | 防止修復引入新問題 |
| 7 | **s5-pr-review** | ✅必做 | 僅審查修復邏輯，WARNING 非阻擋 |
| 8 | **s5-fix-optimize** | ⚡可選 | 只有 CRITICAL findings 才執行 |
| 9 | **s6-test-e2e** | ✅必做 | 驗證 bug 場景已修復（含 bug 的特定 flow）|
| 10 | **s6-test-perf** | ⚡可選 | 性能相關 bug 才需要 |
| 11 | **s6-verify-release** | ✅必做 | 確認測試通過 |
| 12 | **s7-build-artifact** | ✅必做 | 編譯 |
| 13 | **s7-release-notes** | ✅必做 | CHANGELOG 增加 Hotfix 條目 |
| 14 | **s7-deploy** | ✅必做 | 優先部署（通常跳過普通審批流程）|
| 15 | **s7-telemetry** | ✅必做 | 監控確認 bug 消失 |

**跳過**：Stage 0、Stage 1、Stage 2、Stage 3 全段、s6-test-integration（非架構變更）

---

## 對照摘要表

| 情境 | s0-grill | s0-grill-docs | Stage 1 | s2-vision | s2-align | Stage 3 | Stage 4 | Stage 5 | Stage 6 | Stage 7 |
|------|:--------:|:-------------:|:-------:|:---------:|:--------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| 1️⃣ 全新項目（模糊+無代碼） | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2️⃣ 腳手架+模糊需求 | ✅ | ✅ | ⚡ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3️⃣ 腳手架+清晰需求 | ⚡ | ⚡ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4️⃣ Legacy+清晰+陌生架構 | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5️⃣ Legacy+清晰+熟悉架構 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| 6️⃣ Bug Fix（Hotfix） | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⚡ | ⚡ | ✅ |

> **圖例**：✅ 必做 ／ ⚡ 可選（視情況）／ ⬜ 跳過

---

## 快速決策樹

```
需求清晰嗎？
├─ 否 → 有代碼庫嗎？
│        ├─ 否 → 情境 1️⃣（全部 28 skills）
│        └─ 是 → 情境 2️⃣（s0-grill-docs 先行，Stage 1 可選）
│
└─ 是 → 是 Bug 修復嗎？
         ├─ 是 → 情境 6️⃣（Hotfix Mode，11-15 skills）
         └─ 否 → 有代碼庫嗎？
                  ├─ 否（腳手架）→ 情境 3️⃣（跳過 Stage 1 + vision）
                  └─ 是 → 熟悉架構嗎？
                           ├─ 否 → 情境 4️⃣（雙 s0 + refactor mode）
                           └─ 是 → 情境 5️⃣（s-fast-track，17 skills）
```

---

## Skill 數量對比

| 情境 | 使用 Skill 數 | 節省比例（vs 情境 1）|
|------|:------------:|:-------------------:|
| 1️⃣ 全新項目 | 28 | — |
| 2️⃣ 腳手架+模糊 | 26–28 | 0–7% |
| 3️⃣ 腳手架+清晰 | 21–22 | 21–25% |
| 4️⃣ Legacy+陌生 | 22–23 | 18–21% |
| 5️⃣ Legacy+熟悉 | 17 | 39% |
| 6️⃣ Bug Fix | 11–15 | 46–61% |
