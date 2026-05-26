# Skill Coverage Matrix — 2026-05-26

**目的**：確認每個技能的設計原則依據，以及與四大參考倉庫相似技能的對應關係，以識別多餘與缺失的技能。

**設計原則依據**：
- `references/skill-design-intent.md` — C1a/C1b/C1c/C2/C3/C4 結構要求
- `references/scoring-rubric.md` — 6 品質指標（衝突防禦/雙向阻斷/輸入清洗/漸進披露/優雅降級/漂移監控）

**參考倉庫**（`github_skill_sample/` 下）：
- **mattpocock** — `skills/` (engineering + productivity)，共 14 個有效 skill
- **superpowers** — `superpowers/skills/`，共 14 個 skill
- **gstack** — `gstack/` 的各 slash 資料夾，SDLC 相關：/review /plan-eng-review /qa /ship /investigate /health /document-generate /design-consultation /learn
- **OpenSpec** — 工具/格式系統（opsx: 命令），**非 skill 集合**；`openspec/specs/` 是 OpenSpec 自描述規格，不可重用為通用 skill

**判定分類**：
- `essential` — 意圖獨特、原則符合，無可替代
- `redundant-internal` — 與我們自己的另一個技能重複
- `redundant-external` — 四大倉庫有更完整版本，我們的是縮水版
- `needs-evolution` — 意圖對但與參考實作有明顯差距

---

## 主表：37 技能 × 原則依據 × 參考對照

<!-- 待填：每格 = 技能名 + 一句理由，或 — -->

| 技能 | 意圖（1句） | 原則依據 | mattpocock 參考 | superpowers 參考 | gstack 參考 | OpenSpec 參考 | 分類 | 關鍵缺口/備註 |
|------|------------|----------|----------------|-----------------|------------|--------------|------|--------------|
| **s-fast-track** | 根據意圖信號路由到正確 skill，繞過手動選擇 | C3 trigger語言；Skill Index | — | using-superpowers/ (同為 meta entry-point；機制不同：Skill Index vs 隨機觸發) | — | — | essential | Skill Index 機制是我們獨有的 |
| **s0-brainstorm** | 從模糊感受出發，Socratic問答探索問題空間，輸出 problem-draft.md | scoring C1衝突防禦；C2雙向阻斷 | — | brainstorming/ (superpowers 直接出設計文件→writing-plans；我們出 problem-draft→s2 pipeline) | — | — | essential | 觸發條件不同：我們處理「模糊感受」，superpowers 處理「有想法但未設計」 |
| **s0-eval-alignment** | 批次掃描所有 skill 的結構對齊度，輸出 drift 報告 | C1a/C2/C3/C4 全套；C6漂移監控 | — | writing-skills/ (驗證單一 skill；我們是批次掃描所有) | — | — | essential | 四大倉庫均無批次結構對齊掃描工具 |
| **s0-eval-skill** | 單一 skill 的六維品質評估 | scoring 6指標全套 | write-a-skill/ (創建新 skill；eval-skill 評估既有 skill) | writing-skills/ (含驗證步驟，但無六維量化評分) | — | — | essential | 六維量化評分框架是我們獨有的 |
| **s0-semantic-validate** | 驗證技能描述的語義邊界，防止路由混亂 | scoring C1衝突防禦；C3 trigger語言 | — | — | — | — | essential | 四大倉庫均無語義邊界驗證工具 |
| **s0-skill-budget** | 三軸 Token 預算審計（D/I/S），確保 skill 精簡 | C4漸進披露；C3描述精準度 | — | — | — | — | essential | 四大倉庫均無 token 預算審計工具 |
| **s0-trace-feature** | 跨 stage 追蹤某功能的完整實現路徑 | C2 artifact chain | — | — | — | — | essential | 四大倉庫均無跨 stage feature 追蹤工具 |
| **s0-grill** *(新)* | 對任意計畫/設計進行決策樹壓力測試，無 pipeline 依賴 | C1衝突防禦；scoring C2雙向阻斷 | grill-me/ (standalone 決策樹訪談，意圖高度一致) | — | — | — | essential | standalone 版本填補 s2-align-req 的非 pipeline 觸發缺口；兩者並存 |
| **s0-grill-docs** *(新)* | 比對代碼術語與 CONTEXT.md，挑戰漂移並原地更新 | C1衝突防禦；C2 Reads/Writes | grill-with-docs/ (代碼交叉比對+inline CONTEXT.md 更新，意圖一致) | — | — | — | essential | 演進期術語漂移工具；s1-config-context（建立期）保持不變 |
| **s1-config-context** | 定義專案詞彙與 AI 代理上下文邊界（CONTEXT.md） | C2 Reads/Writes；C1衝突防禦 | grill-with-docs/ (都建立 CONTEXT.md；但 grill-with-docs 額外做代碼交叉比對+inline 術語挑戰) | — | — | — | essential | 建立期工具（無代碼）設計正確；演進期術語漂移由新的 `s0-grill-docs` 填補 |
| **s1-define-rules** | 建立專案根本規則（RULES.md，編碼規範/架構） | C1a HARD-GATE；C2 | — | — | — | — | essential | 四大倉庫均無對應的根本規則建立技能 |
| **s1-git-guardrails** | 設定 git 安全欄杆（hooks/branch 保護） | C1-exempt standalone；C5優雅降級 | misc/git-guardrails-claude-code (高度重疊：都設 PreToolUse hooks 阻擋危險 git 命令) | — | — | — | essential | 讀 SKILL.md 確認：我們有完整 HARD-GATE + Completion Report + Step 0 prereq 結構；mattpocock 版本是無結構的 misc 腳本 |
| **s1-lock-tech-stack** | 鎖定技術棧與依賴版本（語言/框架/鎖文件） | C1b stage-boundary approval；C2 | — | — | — | — | essential | 四大倉庫均無對應的技術棧鎖定技能 |
| **s2-capture-vision** | 從用戶原始想法擷取結構化 vision.md | C1c auto-proceed；C2 | — | brainstorming/ (superpowers 也做 idea→設計，但輸出格式和後續路徑不同) | — | — | essential | 我們有明確的 vision.md artifact 格式，這是 pipeline 的起點 |
| **s2-align-req** | 消除 vision 衝突、窮舉決策樹，輸出 alignment.md | C1c；C2；scoring C1-C3 | grill-me/ (決策樹窮舉技術已吸收；但 grill-me 是 standalone，可針對任意計畫) | — | — | — | essential | standalone 缺口由新的 `s0-grill` 填補；s2-align-req 保持 pipeline-locked 設計不變 |
| **s2-struct-req** | 將對齊結果結構化為 REQ+AC 格式需求規格 | C1c；C2；C3 | to-prd/ (to-prd 從對話合成 PRD；我們從 alignment.md 產出 REQ+AC；意圖層不同) | writing-plans/ (writing-plans 更偏實作計畫；struct-req 偏需求規格) | — | — | essential | REQ+AC 格式是我們 pipeline 的核心契約格式 |
| **s2-snapshot-ctx** | 沉澱需求快照到 CONTEXT_SNAPSHOT（S2→S3 gate） | C1b stage-boundary approval；C2 | handoff/ (handoff 給人類開發者交接文件；snapshot-ctx 是 AI pipeline 快照，受眾不同) | — | — | — | essential | pipeline gate 功能是我們獨有的；handoff 是不同受眾 |
| **s3-eval-system** | 評估現有系統影響範圍（blast radius / Schema / API） | C1c；C2；C4 Red Flag | zoom-out/ (zoom-out 做模組映射+呼叫者視圖；eval-system 做衝擊範圍+紅旗評估) | — | /plan-eng-review (plan-eng-review 做架構+邊界案例評審；eval-system 更聚焦衝擊量化) | — | essential | Red Flag 表格是我們獨有的高風險決策攔截機制 |
| **s3-design-arch** | 設計技術方案（ADR / API Contract / 架構決策），雙模式 | C1c；C2 | improve-codebase-architecture/ (前者新設計視角；後者既有代碼重構視角，已加入 Mode B) | — | /plan-eng-review + /design-consultation (gstack 做架構評審+設計系統諮詢) | — | essential | 已加入 `refactor-existing` 模式（Mode B）：讀既有代碼+ADR→架構評估→OpenSpec 改進方案 |
| **s3-breakdown-wbs** | 將技術設計原子化拆解為獨立 WBS 任務 | C1c；C2 | to-issues/ (to-issues 直接發佈到議題追蹤器；我們產出 WBS 文件) | writing-plans/ (writing-plans 也產出細粒度任務清單，但含更多文件清單細節) | — | — | essential | WBS + OpenSpec 格式是我們 pipeline 契約，to-issues 是不同輸出目標 |
| **s3-build-dag** | 建立任務依賴拓撲（DAG），作為 S3→S4 gate | C1b stage-boundary approval；C2 | — | writing-plans/ (含依賴感知排序，但無明確 DAG 格式或 topological sort) | — | — | essential | 明確 DAG + SkillGraphEngine 整合是我們獨有的 |
| **s4-setup-env** | 初始化研發環境（branch / 沙盒 / 工作區） | C1c；C2 | — | using-git-worktrees/ (superpowers 聚焦工作區隔離；我們更廣含 branch 策略+沙盒初始化) | — | — | essential | 更廣泛的環境初始化範疇 |
| **s4-impl-task** | 並發實現原子任務（業務邏輯 + acceptance criterion） | C1c；C2；C3 | — | executing-plans/ (單線程) + subagent-driven-development/ (雙階段複查：規格合規→代碼品質；我們無此機制) | — | — | essential | 讀 SKILL.md 確認：s4-impl-task → s4-tdd → s4-local-debug 三技能組合已等效兩階段複查；不需要整合 |
| **s4-tdd** | 同步編寫單元測試（TDD / coverage / brownfield） | C1c；C2 | tdd/ | test-driven-development/ (三者意圖高度一致：紅綠重構循環) | — | — | essential | 高度對齊，brownfield 支援是我們的特色 |
| **s4-local-debug** | 本地調試（堆疊追蹤 / 根因 / 復現），作為 S4→S5 gate | C1b stage-boundary approval；C2；C5 | diagnose/ (有紀律的診斷循環，意圖高度一致) | systematic-debugging/ (根因優先，意圖高度一致) | /investigate (鐵律：無根本原因，無修復) | — | essential | 四個版本意圖一致，我們有 pipeline gate 功能作為差異點 |
| **s5-sast-lint** | 靜態代碼分析（SAST / Lint / security / vulnerability） | C1c；C2 | — | — | /health (health 組合 linter+類型檢查器+測試+死代碼，並出加權 0-10 分；我們是純 SAST/Lint 步驟) | — | essential | 我們聚焦 SAST 專項；gstack /health 是更廣的品質儀表板（不同意圖） |
| **s5-audit-rules** | 根本規則合規審查（RULES.md / 架構範式） | C1c；C2；C4 Red Flag | — | — | — | — | essential | RULES.md 合規審查是我們獨有的（四大倉庫無對應） |
| **s5-pr-review** | 代碼評審與意見反饋（diff / drift / review） | C1c；C2；C4 Red Flag | in-progress/review (雙軸：Standards軸+Spec軸；我們無明確雙軸拆分) | requesting-code-review/ (派 subagent 審查) + receiving-code-review/ (有根據地推回) | /review (含 SQL 安全+LLM 信任邊界專項；我們無這些專項) | — | essential | 讀 SKILL.md 確認：Step 1 Scope Drift（Spec 軸）+ Step 2 Logic Review（Standards 軸）已是雙軸；SQL 安全+信任邊界在 Step 3 Security Spot-Check 已有 |
| **s5-fix-optimize** | 排障與結構優化，作為 S5→S6 gate | C1b stage-boundary approval；C2；C5 | — | — | — | — | essential | pipeline gate 功能是我們獨有的 |
| **s6-test-integration** | 自動化整合測試（module / coverage / gate） | C1c；C2 | — | — | /qa (gstack qa 含整合層；但 /qa 是更廣的 QA，含 UI+功能) | — | essential | 我們聚焦整合測試層；/qa 是全棧 QA（不同範疇） |
| **s6-test-e2e** | 端到端與邊界驗證（Playwright / user flow / edge case） | C1c；C2 | — | verification-before-completion/ (都要求執行命令並看輸出；superpowers 是 standalone 的通用驗證) | /qa (gstack qa standard/exhaustive 模式涵蓋 e2e) | — | essential | Playwright 專項是我們的特色 |
| **s6-test-perf** | 效能與壓力測試（P50/P95/P99 / throughput / SLO） | C1c；C2 | — | — | — | — | essential | 四大倉庫均無對應的效能測試技能 |
| **s6-verify-release** | 結果最終驗證（release gate / traceability），作為 S6→S7 gate | C1b stage-boundary approval；C2；C4 Red Flag | — | verification-before-completion/ (standalone 通用驗證；我們是 pipeline S6→S7 gate) | /qa-only (gstack report-only 模式；我們是正式 release gate) | — | essential | pipeline gate + traceability 功能是我們獨有的 |
| **s7-build-artifact** | 構建與封裝（artifact / SHA-256 / 版本） | C1c；C2 | — | finishing-a-development-branch/ (finishing 是 merge/PR/棄置決策點；build-artifact 是具體封裝步驟) | /ship (ship 含版本碰撞+CHANGELOG+PR，涵蓋我們的 build+deploy+release-notes) | — | essential | SHA-256 完整性校驗是我們的特色 |
| **s7-deploy** | 生產環境部署（smoke test / dry-run / rollout） | C1c；C2；C5 | — | finishing-a-development-branch/ (兩者都在完成後決定如何集成；superpowers 無 smoke test) | /ship (ship 含 push+PR；我們有 dry-run+rollout 更多生產細節) | — | essential | dry-run + rollout 策略是我們的生產級特色 |
| **s7-release-notes** | 變更日誌沉澱（CHANGELOG / commit / 版本） | C1c；C2 | — | — | /ship (ship 含 CHANGELOG 更新；但我們是獨立步驟，可單獨執行) | — | essential | 獨立步驟允許 CHANGELOG-only 執行 |
| **s7-telemetry** | 運維監控與反饋閉環，作為 End-of-cycle gate | C1b stage-boundary approval；C2；C6 | — | — | /learn (learn 管理跨 session 學習；telemetry 做即時監控+異常偵測+next_cycle_inputs) | — | essential | next_cycle_inputs 閉環機制是我們獨有的 |

---

## 缺口表：參考倉庫有，我們缺的技能

<!-- 待填：agent 回報後補充 -->

| 技能名（參考倉庫） | 倉庫 | 我們最接近的技能 | 意圖差距描述 | 優先級 |
|------------------|------|----------------|------------|--------|
| **grill-me** | mattpocock | s2-align-req | grill-me 是 standalone，可針對任意計畫/設計、可探索代碼庫；s2-align-req 鎖在 pipeline 內需要 vision.md 前提 | **P1** |
| **grill-with-docs** | mattpocock | s1-config-context | grill-with-docs 做代碼交叉比對+inline CONTEXT.md 更新+術語挑戰；s1-config-context 明確禁止從代碼推斷 | **P1** |
| **improve-codebase-architecture** | mattpocock | s3-design-arch | 重構視角（既有代碼健康度改進）vs 新設計視角；我們無既有代碼架構改進技能 | **P2** |
| **subagent-driven-development** | superpowers | s4-impl-task | 兩階段複查（規格合規→代碼品質）的多 subagent 協作模式；我們的實現缺少複查機制 | **P2** |
| **dispatching-parallel-agents** | superpowers | — | 多 agent 任務分發策略（3+ 獨立故障/子系統時）；我們無 agent 協作調度技能 | **P2** |
| **document-generate** | gstack | — | 使用 Diataxis 框架生成結構化文件（教程/操作指南/參考/解釋）；我們無文件生成技能 | **P2** |
| **zoom-out** | mattpocock | s3-eval-system | zoom-out 提供模組映射+呼叫者視圖（使用領域詞彙）；eval-system 更聚焦衝擊範圍量化 | P3 |
| **health** | gstack | s5-sast-lint + s5-audit-rules | gstack /health 組合多工具（linter/型別檢查/測試/死代碼）成加權 0-10 分+趨勢追蹤；我們是分離步驟 | P3 |
| **write-a-skill / writing-skills** | mattpocock + superpowers | — | 創建新 skill 的指引技能；s0-eval-skill 只評估不創建 | P3 |
| **prototype** | mattpocock | — | 拋棄式原型驗證（邏輯分支/UI變異）；Vibe Mode 最近但不是獨立技能 | P3 |
| **handoff** | mattpocock | s2-snapshot-ctx | handoff 產出給人類開發者的交接文件（含建議技能）；snapshot-ctx 是 AI pipeline 快照 | P3 |
| **triage** | mattpocock | — | 議題分類狀態機（needs-triage→ready/wontfix）；我們無議題工作流技能 | P4 |
| **caveman** | mattpocock | — | 75% token 壓縮通訊模式；s0-skill-budget 是技能審計，非通訊模式 | P4 |
| **design-consultation** | gstack | — | 完整設計系統諮詢（美學/字體/顏色/佈局）；我們無 UI 設計技能 | P4 |
| using-superpowers | superpowers | — | 如何組合多個 skill 的元技能 | P3 |
| writing-skills | superpowers | — | 幫助用戶寫新 skill 的 meta-skill | P3 |

---

## 內部重複嫌疑

| 技能 A | 技能 B | 重複維度 | 結論 |
|--------|--------|---------|------|
| s0-eval-alignment | s0-eval-skill | 都在評估 skill 品質 | **不重複** — eval-alignment 批次掃描結構（C1~C4），eval-skill 單一 skill 六維品質；範疇和輸出不同 |
| s0-semantic-validate | s0-skill-budget | 都涉及 skill 描述品質 | **不重複** — semantic-validate 驗證語義邊界防混淆，skill-budget 審計 token 效率；維度不同 |
| s0-eval-alignment | s0-semantic-validate | 都觸及 C1 衝突防禦 | **不重複** — eval-alignment 做批次 C1~C4 結構掃描，semantic-validate 做深度語義驗證；目的不同 |
| s2-capture-vision | s0-brainstorm | 都在需求開始前引導用戶 | **不重複** — brainstorm 處理「模糊感受/問題探索」，capture-vision 處理「有想法→結構化」；前者在後者的上游 |
| s3-eval-system | s5-audit-rules | 都在評估現有狀態 | **不重複** — eval-system 評估衝擊範圍（技術視角），audit-rules 評估規則合規（規範視角）；觸發時間點不同（S3 vs S5） |
| s5-sast-lint | s5-audit-rules | 都在 Stage 5 做檢查 | **不重複** — sast-lint 做靜態代碼安全分析，audit-rules 做 RULES.md 規則合規；工具和目標不同 |
| s4-local-debug | s5-fix-optimize | 都在處理問題 | **不重複** — local-debug 是 S4 的除錯（找根因），fix-optimize 是 S5 的優化修復（已知問題後的結構改善）；時間點不同 |

**結論：37 個技能中無內部重複。**

---

## 分析摘要

**掃描結果**（基於四大倉庫 + 三份設計原則文件）

| 分類 | 數量 | 技能列表 |
|------|------|---------|
| **essential** | 37 | s-fast-track, s0-brainstorm, s0-eval-alignment, s0-eval-skill, s0-semantic-validate, s0-skill-budget, s0-trace-feature, **s0-grill** *(新)*, **s0-grill-docs** *(新)*, s1-config-context, s1-define-rules, s1-git-guardrails, s1-lock-tech-stack, s2-capture-vision, s2-align-req, s2-struct-req, s2-snapshot-ctx, s3-eval-system, s3-design-arch, s3-breakdown-wbs, s3-build-dag, s4-setup-env, s4-impl-task, s4-tdd, s4-local-debug, s5-sast-lint, s5-audit-rules, s5-pr-review, s5-fix-optimize, s6-test-integration, s6-test-e2e, s6-test-perf, s6-verify-release, s7-build-artifact, s7-deploy, s7-release-notes, s7-telemetry |
| **needs-evolution** | 0 | — |
| **redundant-internal** | 0 | — |
| **redundant-external** | 0 | — |

**結論：37 個技能全部有獨立存在理由，無一多餘。6 個初始判定的 needs-evolution 在閱讀 SKILL.md 後全數修正：3 個為誤判（multi-skill 組合已覆蓋），3 個缺口透過新建 s0-grill、s0-grill-docs 和演化 s3-design-arch 填補。**

**缺口行動狀態（2026-05-26 更新）**：

| 優先級 | 建議新技能 | 狀態 |
|--------|----------|------|
| **P1** ✅ | `s0-grill` — standalone 決策樹訪談 | **已完成** — `skills/s0-grill/SKILL.md` 建立；schema 已登記 |
| **P1** ✅ | `s0-grill-docs` — 代碼錨定術語挑戰 | **已完成** — `skills/s0-grill-docs/SKILL.md` 建立；schema 已登記 |
| **P1** ✅ | `s3-design-arch` 加入重構模式 | **已完成** — `refactor-existing` Mode B 已加入 SKILL.md |
| **P2** | `s0-doc-generate` — 結構化文件生成 | 待辦 — 參考 gstack /document-generate + Diataxis 框架 |
| **P2** (誤判) | `s4-impl-task` 演化 | **取消** — s4-impl-task → s4-tdd → s4-local-debug 組合已等效；無需演化 |
| **P2** (誤判) | `s5-pr-review` 演化 | **取消** — SKILL.md 已有雙軸 + SQL/信任邊界；無需演化 |

**OpenSpec 的定位**：是工具/格式系統，不是 skill 集合。其 `artifact-graph`（proposal→design→tasks）與我們的 s2→s3 pipeline 概念重疊，可作為 pipeline 文件格式的參考，但不需要新增技能。
