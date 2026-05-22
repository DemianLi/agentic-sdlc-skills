# Agentic SDLC Skills（敏捷開發流程技能系統）

34 個原子化 Skill 檔案，驅動 AI Agent 走過一套結構化、有門控的軟體開發生命週期。核心管線分 7 個 Stage（基礎建置 → 發布）；5 個獨立的 Stage 0 技能可在任何時間點使用；1 個快速通道路由技能讓你在處理小型任務時跳過 s1–s3 的需求儀式。

每個 Skill 是一個 Markdown 檔案，定義了**角色（Role）**、**工作流（Workflow）**和 **`<HARD-GATE>`** — 一個強制停止點，在指定 artifact 存在於磁碟之前，阻止 Agent 繼續執行。

---

## 為什麼需要這個系統

AI Agent 速度快，但缺乏紀律。沒有門控時，它們會：
- 跳過影響分析，直接從需求跳到寫程式碼
- 在寫失敗測試之前就寫生產代碼
- 自行通過品質門控然後推送到生產環境

這套 Skill 系統強制 Agent 像資深工程團隊一樣工作：**產出 artifact、呈現、推進** — 只在最關鍵的七個 Stage 邊界點要求人工確認。

---

## Stage 0 — 獨立技能（隨時可用）

這五個技能在 s1–s7 管線之外運作，產出的 artifact 可選擇性地注入管線，但不會阻斷或門控管線。

| 指令 | 用途 | 輸出可注入 |
|---|---|---|
| `/s0-brainstorm` | 探索問題空間，產出框架化問題陳述 | `/s2-capture-vision` |
| `/s0-trace-feature` | 追蹤既有功能的呼叫鏈，產出 Mermaid 序列圖 | `/s3-eval-system` 或 `/s2-capture-vision` |
| `/s0-eval-skill` | 依 6 項結構品質標準審核單一技能 | 技能作者修復漂移 |
| `/s0-eval-alignment` | 批次掃描所有 28 個 s1–s7 技能的設計意圖對齊度 | 維護者執行修復 |
| `/s0-skill-budget` | 合併任何 SKILL.md 前，依三軸（D 描述精確度、I 索引覆蓋率、S 檔案大小）審核 token 效率 | 技能作者修復後合入 |

---

## 快速通道路由

對於不需要完整 s1–s3 需求儀式的任務：

| 指令 | 使用時機 |
|---|---|
| `/s-fast-track` | 修 Bug、單檔修改、Brownfield 功能新增、快速原型 — 問一個澄清問題後直接路由到正確的 s4 技能 |

`/s-fast-track` 支援三種**開發模式**，由任務描述中的意圖訊號選擇：

| 模式 | 觸發訊號 | TDD | s5 審查 | Commit 要求 |
|---|---|---|---|---|
| **Standard（標準）** | *（無）* | 鐵律強制執行 | 完整流程 | 正常 |
| **Vibe Mode（探索模式）** | `--vibe`、"prototype"、"throwaway"、"spike" | 選用（直接路由至 `/s4-impl-task`） | 跳過 | 必須加 `[WIP/Prototype]` 標籤 |
| **Hotfix Mode（熱修復模式）** | `--hotfix`、"quick fix"、"legacy codebase" | 鐵律強制執行 | 僅審 CRITICAL | 正常 |

模式訊號**優先於**任務類型路由。Vibe Mode 在執行前需要明確的 Y/n 確認。Standard 模式行為與之前完全相同。

---

## 7 Stage 管線

```
Stage 1              Stage 2              Stage 3              Stage 4
基礎建置           →  產品管理           →  系統架構           →  實作
Foundation             Product Manager       System Architect      Implementer
RULES.md               vision.md             design.md             Code + tests
CONTEXT.md             alignment.md          wbs.md                TASK_DAG [x]
<技術棧鎖定>           requirements.md       TASK_DAG.md
                       CONTEXT_SNAPSHOT.md

Stage 5              Stage 6              Stage 7
代碼審查           →  QA 測試            →  發布管理
Code Auditor           QA Engineer           Release Manager
SAST 報告              test-results.json     Artifact + tag
架構審計報告           整合測試通過          CHANGELOG.md
PR 審查報告            E2E 通過              遙測報告
```

每個箭頭是一次**交接（Handoff）** — 一組已提交的 artifact，下一個 Stage 開始前必須全部存在。詳見 `HANDOFF.md` 的完整驗收標準。

---

## 全部 34 個技能

| Stage | 角色 | 指令 | 用途 |
|---|---|---|---|
| *(快速通道)* | 路由器 | `/s-fast-track` | 修 Bug 和小型任務跳過 s1–s3，路由到對應的 s4 技能 |
| 0 *(獨立)* | 問題偵探 | `/s0-brainstorm` | 探索問題空間，產出框架化問題陳述 |
| 0 *(獨立)* | 代碼考古學家 | `/s0-trace-feature` | 追蹤既有功能呼叫鏈，產出 Mermaid 序列圖 |
| 0 *(獨立)* | 技能審計員 | `/s0-eval-skill` | 依 6 項結構品質標準審核單一技能 |
| 0 *(獨立)* | 對齊審查員 | `/s0-eval-alignment` | 批次掃描所有 s1–s7 技能的設計意圖漂移 |
| 0 *(獨立)* | Token 預算審計員 | `/s0-skill-budget` | 合併前依 D/I/S 三軸審核任何新增或修改的技能 |
| 1 | 基礎建置工程師 | `/s1-define-rules` | 撰寫 `RULES.md`（Lint 規則、目錄結構、禁止模式） |
| 1 | 基礎建置工程師 | `/s1-config-context` | 撰寫領域詞彙表 `CONTEXT.md`，定義 AI 邊界 |
| 1 | 基礎建置工程師 | `/s1-lock-tech-stack` | 鎖定執行環境與框架版本，產生 lock 檔 |
| 1 | 基礎建置工程師 | `/s1-git-guardrails` | 安裝 PreToolUse hook，在執行前攔截破壞性 git 指令 |
| 2 | 產品經理 | `/s2-capture-vision` | 收集問題陳述、目標用戶、解決方案方向 |
| 2 | 產品經理 | `/s2-align-req` | 解決利害關係人衝突，定義範圍邊界 |
| 2 | 產品經理 | `/s2-struct-req` | 撰寫含二元驗收標準的結構化需求 |
| 2 | 產品經理 | `/s2-snapshot-ctx` | 產出 `CONTEXT_SNAPSHOT.md`（Stage 3 的迭代種子） |
| 3 | 系統架構師 | `/s3-eval-system` | 掃描代碼庫，分類爆炸半徑（🔴/🟡/🟢），撰寫影響報告 |
| 3 | 系統架構師 | `/s3-design-arch` | 撰寫含 Mermaid 序列圖的 OpenSpec 設計文件 |
| 3 | 系統架構師 | `/s3-breakdown-wbs` | 將設計拆解為原子任務（每個 ≤5 分鐘） |
| 3 | 系統架構師 | `/s3-build-dag` | 建立依賴 DAG，識別關鍵路徑，撰寫 `TASK_DAG.md` |
| 4 | 實作工程師 | `/s4-setup-env` | 從 DAG 選取任務，設置 branch 和執行環境 |
| 4 | 實作工程師 | `/s4-tdd` | 紅→綠→重構（鐵律：沒有失敗測試就不能寫生產代碼） |
| 4 | 實作工程師 | `/s4-impl-task` | 實作一個原子任務到 GREEN |
| 4 | 實作工程師 | `/s4-local-debug` | 復現→最小化→假設→埋點→修復→迴歸測試 |
| 5 | 代碼審計員 | `/s5-sast-lint` | 執行 SAST 和 Linter，標記 CRITICAL 違規 |
| 5 | 代碼審計員 | `/s5-audit-rules` | 依 `RULES.md` 約束驗證架構合規性 |
| 5 | 代碼審計員 | `/s5-pr-review` | 範圍漂移偵測，嚴重性分級（CRITICAL/WARNING/SUGGESTION） |
| 5 | 代碼審計員 | `/s5-fix-optimize` | 自動修復 CRITICAL 問題；效能優化 |
| 6 | QA 工程師 | `/s6-test-integration` | 執行整合測試，驗證所有關鍵路徑通過 |
| 6 | QA 工程師 | `/s6-test-e2e` | 執行 Playwright/Cypress，驗證主要用戶流程 |
| 6 | QA 工程師 | `/s6-test-perf` | 執行 k6/Artillery，捕捉 P50/P95/P99，迴歸門控（20%） |
| 6 | QA 工程師 | `/s6-verify-release` | 執行完整測試套件，寫入 `test-results.json`，發出 PASS 或 BLOCKED |
| 7 | 發布經理 | `/s7-build-artifact` | 建構、打標籤、簽署發布 artifact |
| 7 | 發布經理 | `/s7-deploy` | 部署 → smoke test → 驗證（支援 dry-run 模式） |
| 7 | 發布經理 | `/s7-release-notes` | 依 Keep a Changelog 格式產生 `CHANGELOG.md` |
| 7 | 發布經理 | `/s7-telemetry` | 捕捉部署後指標，對比 S6 基準線，將 next_cycle_inputs 回饋 Stage 2 |

---

## HARD-GATE 強制執行機制

每個 Skill 都有一個 `<HARD-GATE>` 區塊，指定 Agent 推進前**必須成立的條件**。系統存在兩種批准模式：

### Stage 邊界門控（7 個技能 — 需要人工確認）

在七個 Stage 轉換點，Agent 的訊息**必須**以下列文字結尾：

> *「Awaiting your approval to proceed to \<next-skill\>.」*

在人類明確批准前，Agent 不得產生下一 Stage 的 artifact、代碼或分析。沉默的回應**不等於**批准。

| 技能 | 轉換點 |
|---|---|
| `/s1-lock-tech-stack` | Stage 1 → Stage 3 |
| `/s2-snapshot-ctx` | Stage 2 → Stage 3 |
| `/s3-build-dag` | Stage 3 → Stage 4 |
| `/s4-local-debug` | Stage 4 → Stage 5 |
| `/s5-fix-optimize` | Stage 5 → Stage 6 |
| `/s6-verify-release` | Stage 6 → Stage 7 |
| `/s7-telemetry` | 迭代結束 |

### Stage 內部門控（21 個技能 — 自動推進）

在同一 Stage 內，達到 HARD-GATE 條件且呈現 artifact 後，Agent 立即推進到下一個技能，無需等待批准。下一個技能的 HARD-GATE 隨即生效。

### HARD-GATE 阻止的範例

| 技能 | 缺乏證據時阻止的行為 |
|---|---|
| `s1-lock-tech-stack` | 在記錄實際 `python --version` 輸出前產生 lock 檔 |
| `s3-eval-system` | 在影響報告寫入磁碟並 commit 前推進到設計階段 |
| `s4-tdd` | 在貼上實際 `pytest FAILED` 終端輸出前寫生產代碼 |
| `s6-verify-release` | 在 `test-results.json` 由機器產生並 commit 前發出「Ready」信號 |

---

## 安裝方式

Skills 是純 Markdown 檔案，複製到你的 Claude Code 專案作為 slash commands 即可。

**方案 A — 專案本地（推薦）：**
```bash
# 在你的專案根目錄
mkdir -p .claude/skills
cp -r skills/s4-tdd .claude/skills/
```
在該專案的 Claude Code 會話中用 `/s4-tdd` 呼叫。

**方案 B — 全域安裝：**
```bash
cp -r skills/* ~/.claude/skills/
```
在所有 Claude Code 會話中皆可使用。

---

## 使用技能

1. 在專案目錄啟動 Claude Code
2. 輸入 slash command，例如 `/s3-eval-system`
3. Agent 扮演對應角色，執行工作流，產出 artifact
4. **Stage 內**：Agent 自動推進到下一個技能
5. **Stage 邊界**：Agent 停下來 — 審查 artifact，輸入你的批准
6. 進入下一個 Stage

---

## 專案結構

```
skills/
  s-fast-track/         快速通道路由 — 小型任務跳過 s1–s3
  s0-brainstorm/        問題偵探 — 框架化問題陳述
  s0-trace-feature/     代碼考古學家 — 功能呼叫鏈圖
  s0-eval-skill/        技能審計員 — 單一技能結構品質審核
  s0-eval-alignment/    對齊審查員 — 批次漂移偵測（28 個技能）
    scripts/scan.py     可重用 CLI 掃描器（exit 0 = 全部 ALIGNED）
    scripts/engine.py   SkillGraphEngine v2.2 — 拓撲引擎 + CLI
    tests/              冒煙測試夾具 + pytest 套件（test_scan.py + test_engine.py）
  s0-skill-budget/      Token 預算審計員 — 技能撰寫的 D/I/S token 效率門控
  s1-*/SKILL.md         Stage 1 — 基礎建置工程師（4 個技能）
  s2-*/SKILL.md         Stage 2 — 產品經理（4 個技能）
  s3-*/SKILL.md         Stage 3 — 系統架構師（4 個技能）
  s4-*/SKILL.md         Stage 4 — 實作工程師（4 個技能）
  s5-*/SKILL.md         Stage 5 — 代碼審計員（4 個技能）
  s6-*/SKILL.md         Stage 6 — QA 工程師（4 個技能）
  s7-*/SKILL.md         Stage 7 — 發布經理（4 個技能）
schemas/
  skill_graph_schema.yaml   宣告式依賴圖譜 — 28 個技能，含 stage、requires、outputs
  SKILL_INDEX.yaml          關鍵字 → 技能對映，提供 O(1) 路由（供 s-fast-track 和 s0-skill-budget 使用）
references/
  skill-design-intent.md        s0-eval-alignment 的評估基線（C1–C4 規則 + 每個技能的關鍵詞列表）
  SKILL_INDEX_TEMPLATE.yaml     SKILL_INDEX.yaml 的標準模板，內含三步維護清單
docs/
  skill-evals/          對齊掃描報告（YYYY-MM-DD-alignment-scan.md）
  TRIALS_INDEX.md       所有研究試驗索引（07–16），含假設與結果
  TRIAL_*_REPORT.md     個別試驗報告
  BENCHMARK_REFERENCE.md  4 個參考 repo 的設計分析
.github/workflows/
  alignment.yml         CI 門控 — 在 skills/** 變更時執行冒煙測試和對齊掃描
CONTEXT.md              領域詞彙表與通用語言
HANDOFF.md              Stage 間的 artifact 管線與驗收標準
QA.md                   28 步 SDLC 品質清單（設計意圖的原始資料來源）
```

> **分支說明**：`main` 只包含 skills 和文件。`research` 分支另外包含 `test_projects/` — 10 次試驗執行（07–16），含完整源碼、測試和建構 artifact。

---

## Skill 解剖

每個 `SKILL.md` 有四個區塊：

```
---
name: <技能名稱>
description: >
  Use when/after/at/before/during <觸發條件>  ← 只寫觸發語言，不寫工作流步驟
---

<HARD-GATE>          ← 前置條件 + OUTPUT DISCIPLINE 子句
</HARD-GATE>

<what-to-do>         ← 角色身份 + 分步工作流 + 紅旗表 + 完成報告
</what-to-do>

<supporting-info>    ← 流程圖（Graphviz DOT）、Artifact 標準、Artifact 依賴
</supporting-info>
```

---

## 設計原則

- **Artifact 優先** — 每個 Stage 產出已提交的檔案，而不只是對話
- **垂直切片** — Stage 4 每次只實作一個行為（紅→綠→重構）
- **Stage 邊界人工確認** — 七個 Stage 轉換點需要明確批准；Stage 內部步驟自動推進，減少儀式感而不犧牲安全性
- **證據優於斷言** — Agent 必須貼出實際終端輸出，不能只聲稱成功
- **阻塞的交接向後升級** — 若 artifact 缺失，Agent 回報 `NEEDS_CONTEXT` 並停止；絕不向前推測
- **Description 是觸發器，不是摘要**（Matt Pocock 原則）— 每個技能的 `description` 欄位只說明*何時*使用；不在此處摘要工作流步驟，確保 Agent 永遠讀取完整的 `<what-to-do>` 主體
- **Brownfield 感知** — `s4-tdd` 偵測 `RULES.md` 中的 `mode: brownfield`，將覆蓋率門控範圍縮小到新增/修改的行，避免在老舊代碼上累積覆蓋率債務
- **Token 預算與規模解耦** — `SKILL_INDEX.yaml` 提供 O(1) 關鍵字路由；`s0-skill-budget` 在合併前強制執行 D/I/S 三軸審核。無論系統新增多少技能，每次任務的定位成本恆為 ~200 tokens（索引）+ 單一技能全文，不隨技能總數線性增長

---

## 對齊工具

隨時執行掃描器，驗證所有技能仍符合其原始設計意圖：

```bash
# 完整掃描 — 終端輸出
python3 skills/s0-eval-alignment/scripts/scan.py

# 單一 Stage
python3 skills/s0-eval-alignment/scripts/scan.py --stage s6

# 寫入帶日期的報告到 docs/skill-evals/
python3 skills/s0-eval-alignment/scripts/scan.py --write
```

掃描器對每個技能檢查四個維度：

| 檢查 | 驗證內容 |
|-------|-----------------|
| **Q** — QA.md 對齊 | 技能主體中存在 ≥ 3 個設計意圖關鍵詞 |
| **C1** — HARD-GATE | `<HARD-GATE>` 存在；邊界技能以「Awaiting your approval」結尾；Stage 內技能有「proceed immediately to」 |
| **C2** — Artifact 鏈 | `<supporting-info>` 明確聲明 **Reads** 和 **Writes** |
| **C3** — 觸發語言 | `description` 不含工作流步驟或流程動詞 |

若所有技能 ALIGNED 則 exit `0`；若有任何 PARTIAL 或 DRIFTED 則 exit `1`（CI 友善）。

### CI 強制執行

GitHub Actions 工作流（`.github/workflows/alignment.yml`）在每次涉及 `skills/**` 的 PR 和 push 時自動執行：

1. **冒煙測試** — `pytest skills/s0-eval-alignment/tests/ -v`（aligned + drifted 夾具）
2. **對齊掃描** — `python3 skills/s0-eval-alignment/scripts/scan.py`（exit 1 → 如有技能漂移則阻斷合併）
3. **帶日期的報告** — push 到 `main` 時，寫入 `docs/skill-evals/YYYY-MM-DD-alignment-scan.md` 並作為 GitHub Actions artifact 上傳

本地執行冒煙測試：

```bash
pip install pytest
pytest skills/s0-eval-alignment/tests/ -v
```

---

## Skill Graph Engine

`schemas/skill_graph_schema.yaml` 是技能依賴關係的宣告式原始資料來源。`SkillGraphEngine`（`skills/s0-eval-alignment/scripts/engine.py`）在執行時讀取此 schema，回答三個問題：

- **已完成什麼？** — 透過 glob 比對每個技能的 `outputs` 進行檔案系統檢測，支援手動覆蓋
- **下一步是什麼？** — 所有上游依賴均已滿足的技能
- **什麼被阻塞？** — 至少有一個上游依賴未滿足的技能

```bash
# 顯示完整狀態（已完成 / 下一步 / 被阻塞）
python3 skills/s0-eval-alignment/scripts/engine.py --status

# 只列出下一個可執行的技能
python3 skills/s0-eval-alignment/scripts/engine.py --next

# 列出被阻塞的技能及其缺少的依賴
python3 skills/s0-eval-alignment/scripts/engine.py --blocked

# 驗證 schema（循環依賴、未定義依賴、欄位名稱拼寫錯誤）
python3 skills/s0-eval-alignment/scripts/engine.py --validate

# strict 模式 — 只有在所有遞移依賴也完成時才標記為完成
python3 skills/s0-eval-alignment/scripts/engine.py --status --mode strict

# 壓縮輸出 — 將阻塞清單折疊為每 Stage 的計數
python3 skills/s0-eval-alignment/scripts/engine.py --status --compact
```

兩種導航模式：

| 模式 | 行為 |
|---|---|
| `fluid`（預設） | 僅依據檔案系統中 `outputs` 的存在判定完成狀態；被跳過的上游依賴以智慧補足建議的形式呈現，不阻斷執行 |
| `strict` | 只有當所有遞移上游依賴也已完成時，技能才被標記為已完成 |

沒有宣告 `outputs` 的技能（如 `s4-setup-env`）在工作區根目錄存在 **哨兵檔案**（sentinel file）`.{skill-name}.done` 時標記為完成。

單元測試：`skills/s0-eval-alignment/tests/test_engine.py`（426 行 — 覆蓋拓撲排序、循環偵測、fluid/strict 模式、哨兵檔案、繞道依賴報告）。

---

## 完成狀態詞彙表

每個 Skill 以且僅以下列狀態之一結束：

| 狀態 | 含義 |
|---|---|
| `DONE` | Artifact 已產出並提交，已批准（或 Stage 內自動推進） |
| `DONE_WITH_CONCERNS` | 完成，但列出了可能影響下一 Stage 的具體疑慮 |
| `BLOCKED` | 無法推進；已明確說明阻塞點；重試前必須修復 |
| `NEEDS_CONTEXT` | 上游 artifact 缺失；暫停直到提供 |
