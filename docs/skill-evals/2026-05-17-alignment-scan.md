# Alignment Scan Report
**掃描範圍**: `skills/s1-*` 至 `skills/s7-*`（28 個 skill）
**Date**: 2026-05-17
**Evaluator**: s0-eval-alignment
**基線**: `skills/s0-eval-alignment/references/skill-design-intent.md`

---

## 總覽表

| Skill | Step | Q 對齊 | C1 強制執行 | C2 工件鏈 | C3 Description | 整體 |
|-------|------|--------|------------|----------|----------------|------|
| s1-define-rules | 1.1 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s1-config-context | 1.2 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s1-lock-tech-stack | 1.3 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s1-git-guardrails | 1.1 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s2-capture-vision | 2.1 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s2-align-req | 2.2 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s2-struct-req | 2.3 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s2-snapshot-ctx | 2.4 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s3-eval-system | 3.1 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s3-design-arch | 3.2 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s3-breakdown-wbs | 3.3 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s3-build-dag | 3.4 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s4-setup-env | 4.1 | ⚠️ | ✅ | ✅ | ✅ | ⚠️ PARTIAL |
| s4-impl-task | 4.2 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s4-tdd | 4.3 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s4-local-debug | 4.4 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s5-sast-lint | 5.1 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s5-audit-rules | 5.2 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s5-pr-review | 5.3 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s5-fix-optimize | 5.4 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s6-test-integration | 6.1 | ⚠️ | ✅ | ✅ | ✅ | ⚠️ PARTIAL |
| s6-test-e2e | 6.2 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s6-test-perf | 6.3 | ⚠️ | ✅ | ✅ | ✅ | ⚠️ PARTIAL |
| s6-verify-release | 6.4 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s7-build-artifact | 7.1 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |
| s7-release-notes | 7.2 | ⚠️ | ✅ | ✅ | ✅ | ⚠️ PARTIAL |
| s7-deploy | 7.3 | ⚠️ | ✅ | ✅ | ✅ | ⚠️ PARTIAL |
| s7-telemetry | 7.4 | ✅ | ✅ | ✅ | ✅ | ✅ ALIGNED |

**總計**：23/28 ✅ ALIGNED，5/28 ⚠️ PARTIAL，0/28 ❌ DRIFTED

---

## 強制執行機制掃描（C1–C4）

| 檢查 | 結果 |
|------|------|
| C1 HARD-GATE 存在 | 28/28 ✅ |
| C1 "Awaiting your approval" 結尾 | 28/28 ✅ |
| C2 Reads + Writes 工件鏈聲明 | 28/28 ✅ |
| C3 Description 不含流程描述詞 | 28/28 ✅ |
| C4 紅旗表（4 個高風險 skill）| 4/4 ✅ |

四大倉庫共同洞察的「輸出紀律」在全部 skill 中已完整落地。

---

## PARTIAL 清單（5 個 skill）

### s4-setup-env — Step 4.1

**概念缺口**：QA.md 4.1 明確提到「Git Worktree」和「開發沙盒」，但 skill 只涉及 feature branch checkout，未提及 `git worktree add` 工作流。若專案採用 Worktree 並行開發模式，此 skill 的指引不足。

**現有覆蓋**：`git checkout -b`、branch 驗證、workspace 清潔度確認 ✅

**建議**：在 Step 2 Branch Setup 中補充 Worktree 作為替代選項：
```
git worktree add ../task-N-<slug> -b task-N-<slug>
```

---

### s6-test-integration — Step 6.1

**概念缺口**：QA.md 6.1「將多個原子任務的代碼**合併後**，執行模組間整合測試」— 合併（merge/combine）步驟作為整合測試的前提未在 skill 中明確。AI 可能跳過合併驗證直接跑測試。

**現有覆蓋**：module-to-module 整合測試、blocking 判斷 ✅

**建議**：在 Step 0 加入前提確認：「確認所有待測 Atomic Task 已合併至同一分支，否則 BLOCKED」。

---

### s6-test-perf — Step 6.3

**概念缺口**：QA.md 6.3 點名三種具體失敗模式：記憶體洩漏、資料庫死鎖、響應時間。Skill 涵蓋負載測試工具與 P99 閾值，但未要求明確偵測前兩種失敗模式。

**現有覆蓋**：k6/Artillery/Locust、concurrent users、response time ✅

**建議**：在 Step 2 加入記憶體分析（`memory-profiler`、heap snapshot）與資料庫死鎖偵測（query timeout log 分析）作為可選但推薦的額外測試步驟。

---

### s7-release-notes — Step 7.2

**概念缺口**：QA.md 7.2「變更日誌、**升級指南**與 **API 變更文檔**」。Skill 產出 CHANGELOG.md 條目，但未處理升級指南（breaking changes 的遷移說明）與 API 變更文檔（endpoint 增刪改摘要）。

**現有覆蓋**：git log 解析、CHANGELOG.md（Keep a Changelog 格式）✅

**建議**：在 Step 3 加入判斷：若本次變更包含 breaking changes 或 API 異動，產出額外的 `UPGRADE.md` 段落與 API diff 摘要。

---

### s7-deploy — Step 7.3

**概念缺口**：QA.md 7.3「透過 **GitOps** 或部署工具」。Skill 涵蓋 Docker/k8s/fly.io 直接部署，但未提及 GitOps（ArgoCD/Flux）作為替代路徑，可能讓採用 GitOps 的團隊無從對應。

**現有覆蓋**：dry-run 模式、k8s、fly.io、PyPI、Docker registry ✅

**建議**：在 Deploy Mode Selection 加入 GitOps 路徑：「若團隊使用 ArgoCD/Flux，部署即為 PR 合入 main；smoke test 在 CD pipeline 完成後執行」。

---

## 優先修復建議

| 優先 | Skill | 修復描述 | 影響 |
|------|-------|---------|------|
| 🔴 P1 | s7-release-notes | 補充升級指南與 API 變更文檔輸出邏輯 | breaking changes 無人處理 |
| 🔴 P1 | s6-test-integration | 補充合併前提確認步驟 | 可能跳過跨 task 整合 |
| 🟡 P2 | s6-test-perf | 加入記憶體洩漏與資料庫死鎖偵測指引 | 線上問題漏網 |
| 🟡 P2 | s7-deploy | 補充 GitOps 部署路徑 | GitOps 團隊無法使用 |
| 🟢 P3 | s4-setup-env | 補充 `git worktree` 作為替代工作流 | 並行開發場景缺支援 |

---

## 元發現：Rubric 校準問題

本次掃描發現 **skill-design-intent.md 的關鍵詞列表為純中文**，但 s1-s7 大量 skill 採用**英文術語**（如 `business logic`、`sequence diagram`、`SAST`、`Docker image`）。

初步 grep 將 13 個 skill 標記為 PARTIAL，人工驗證後確認 8 個為**誤判（false negative）**。

**建議行動**：更新 `references/skill-design-intent.md`，為每個關鍵詞補充英文對等詞，例如：

```
資料結構 / data struct / schema
接口 / interface / contract / API
時序 / sequence
記憶體洩漏 / memory leak
```

此修改可讓未來的自動化掃描不需人工複核。

---

*此報告由 s0-eval-alignment 產出。下次掃描建議在任何 s1-s7 skill 有重大改動後執行。*