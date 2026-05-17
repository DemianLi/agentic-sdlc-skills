# Skill Design Intent Map
# 設計意圖對映表 — s0-eval-alignment 的評估基線

> 來源：`QA.md`（28 步驟）× `docs/BENCHMARK_REFERENCE.md`（四大倉庫亮點）
> 更新此檔案即更新評估基線，不需要修改 SKILL.md。

---

## 一、跨 Skill 模式檢查（Cross-Cutting Checks）

以下檢查適用於**所有 s1-s7 skill**。出處來自四大倉庫共同驗證的設計原則。

| 代號 | 檢查項 | PASS 條件 | 出處 |
|------|--------|-----------|------|
| C1 | 強制執行機制 | 有 `<HARD-GATE>` 區塊，且包含 "Awaiting your approval" | 主題 1：輸出紀律（四大倉庫共識） |
| C2 | 工件鏈聲明 | `<supporting-info>` 有 **Reads** 和 **Writes** 明確聲明 | 亮點 3：顯式工件鏈（gstack + OpenSpec） |
| C3 | Description 觸發格式 | description 不含 "Step"、"Workflow"、流程動詞串列 | 亮點 1：Description 精密設計（Matt Pocock + Superpowers） |

**C4 紅旗表（僅適用高風險 skill）**

以下 skill 應有包含 "Red Flag"、"Common Rationalization"、"Stop" 字樣的表格：

```
s3-eval-system, s5-pr-review, s6-verify-release, s5-audit-rules
```

出處：亮點 5（Superpowers + Matt Pocock）。`s4-tdd` 已有，`s0-trace-feature` 已有。

---

## 二、Per-Skill QA.md 步驟對映

評分邏輯：SKILL.md 全文中出現 ≥3 個該步驟的關鍵詞 → **ALIGNED**；1-2 個 → **PARTIAL**；0 個 → **DRIFTED**。

### Stage 1 — 初始化與根本規則定義

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s1-define-rules` | 1.1 | 編碼規範 / coding standard、Lint / lint、架構範式 / architecture pattern、安全性底線 / security baseline、RULES.md |
| `s1-config-context` | 1.2 | context、configure、role / identity、agent、global |
| `s1-lock-tech-stack` | 1.3 | 技術棧 / tech stack、依賴 / dependency、語言版本 / language version、框架 / framework、套件 / package、資料庫 / database |
| `s1-git-guardrails` | 1.1 | git、安全 / security、合規 / compliance、branch、commit、hook |

### Stage 2 — 需求對齊與結構化

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s2-capture-vision` | 2.1 | 構思 / idea、想法 / vision、痛點 / pain point、需求 / requirement、業務 / business、vision |
| `s2-align-req` | 2.2 | 對齊 / align、衝突 / conflict、歧義 / ambiguity、問答 / Q&A、邊界 / boundary、澄清 / clarify |
| `s2-struct-req` | 2.3 | 結構化 / structured、PRD、User Story、Gherkin、BDD、文檔 / document |
| `s2-snapshot-ctx` | 2.4 | snapshot、Context、沉澱、知識 |

### Stage 3 — 技術方案制定與原子化拆解

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s3-eval-system` | 3.1 | 現有系統 / existing system、影響 / impact、代碼 / code、Schema / schema、API、評估 / evaluate |
| `s3-design-arch` | 3.2 | 技術方案 / technical design、Design Doc、資料結構 / data structure / schema、接口 / interface / API contract、時序 / sequence diagram |
| `s3-breakdown-wbs` | 3.3 | 原子化 / atomic、拆解 / breakdown、WBS、最小 / minimal、執行單元 / execution unit |
| `s3-build-dag` | 3.4 | DAG / dag、依賴 / dependency、拓撲 / topology、有向無環 / directed acyclic、並發 / concurrent、順序 / sequence |

### Stage 4 — 開發實現與本地調試

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s4-setup-env` | 4.1 | 環境 / environment、Worktree / worktree、Branch / branch、沙盒 / sandbox、初始化 / init / setup |
| `s4-impl-task` | 4.2 | 原子任務 / atomic task、業務邏輯 / business logic、實現 / implement、核心 / core、規則 / rules |
| `s4-tdd` | 4.3 | test、TDD、pytest、spec、coverage |
| `s4-local-debug` | 4.4 | 編譯 / compile / build、調試 / debug、日誌 / log、Stack Trace / stack trace、錯誤 / error |

### Stage 5 — 代碼審查與靜態驗證

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s5-sast-lint` | 5.1 | Lint / lint、靜態分析 / static analysis、安全掃描 / security scan / SAST、漏洞 / vulnerability、Code Smell / code smell |
| `s5-audit-rules` | 5.2 | 合規 / compliance、規則 / rule、架構準則 / architecture guideline、RULES.md、違規 / violation |
| `s5-pr-review` | 5.3 | PR / pull request、評審 / review、review、意見 / comment、重構 / refactor、邏輯漏洞 / logic bug |
| `s5-fix-optimize` | 5.4 | fix、optimize、resolve、analysis、audit |

### Stage 6 — 動態測試與動態驗證

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s6-test-integration` | 6.1 | 整合測試 / integration test、模組 / module、接口調用 / interface / API call、合併 / merge |
| `s6-test-e2e` | 6.2 | E2E / end-to-end、用戶行為 / user behavior、邊界條件 / boundary / edge case、端對端 / end-to-end |
| `s6-test-perf` | 6.3 | 效能 / performance、壓力 / stress / load、高並發 / concurrent、記憶體 / memory、資料庫 / database |
| `s6-verify-release` | 6.4 | 最終驗證 / final verification、覆蓋率 / coverage、測試報告 / test report、交付 / release |

### Stage 7 — 交付發佈與閉環迭代

| Skill | Step | QA.md 必現關鍵詞（≥3 即 ALIGNED） |
|-------|------|----------------------------------|
| `s7-build-artifact` | 7.1 | 構建 / build、封裝 / package、CI/CD、鏡像 / image / Docker image、發佈檔 / artifact |
| `s7-release-notes` | 7.2 | 變更日誌 / CHANGELOG、Release Notes / release notes、提交記錄 / git log / commit、升級 / upgrade |
| `s7-deploy` | 7.3 | 部署 / deploy / deployment、生產環境 / production、GitOps / gitops / ArgoCD / Flux、推送 / push |
| `s7-telemetry` | 7.4 | 遙測 / telemetry、Telemetry / telemetry、監控 / monitoring、異常 / anomaly、閉環 / feedback loop |

---

## 三、四大倉庫優勢欄位（待填入）

> 此欄位為後續迭代預留。當你完成某個 skill 的借鑒分析後，在此記錄「該 skill 應體現哪個亮點的哪個模式」。

| Skill | 應體現的亮點 | 來源倉庫 | 狀態 |
|-------|------------|---------|------|
| （範例）`s4-tdd` | 亮點 5 紅旗表（已實現）、主題 2 Evidence over Assertion | Superpowers + Matt Pocock | ✅ 已實現 |
| 其他 skill | — | — | 🔲 待填入 |

---

*此檔案是評估基線，修改需同步更新 `tests/expected/` 中的期望輸出。*
