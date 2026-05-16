# 四大倉庫借鑒分析文檔

> 分析對象：gstack · OpenSpec · Matt Pocock Skills · Superpowers
> 分析目的：提取各自的設計優勢與核心思路，應用於本 Agentic SDLC Skills 系統的持續改進

---

## 一、各倉庫定位速覽

| 倉庫 | 定位 | 核心問題 | 主要創新 |
|------|------|---------|---------|
| **gstack** | 完整虛擬工程隊伍 | AI 代理無方向性、工作流碎片化 | 結構化角色 × 顯式工件鏈 × 模板代碼生成 |
| **OpenSpec** | 人機共識規格層 | 規格漂移、上下文喪失、棕田開發缺支持 | Delta Specs × 工件 DAG × Schema 驅動 |
| **Matt Pocock Skills** | 工程實踐外部化 | AI 跳過設計/測試直接寫代碼 | 認知流程編碼化 × 硬/軟依賴二分 |
| **Superpowers** | 強制執行的工程方法論 | AI rationalization 逃避檢查點 | 強制語言 × 紅旗表 × Skills 測試框架 |

---

## 二、核心設計哲學對比

### gstack — 「結果即系統」

gstack 的核心哲學是：**不是工具集，而是軟體製造系統**。它以 240× 年輸出量（2013→2026）作為設計目標的量化依據。

關鍵洞察（ETHOS.md）：

> "The point isn't who typed it, it's what shipped."

三層知識層次作為執行引擎：
- **Layer 1 Tried & True** — 成熟模式，成本近零，风险是「假設明顯就是對的」
- **Layer 2 New & Popular** — 當前最佳實踐，需主動搜索、批判審視
- **Layer 3 First Principles** — 從問題本身推導，最珍貴。當第一性原理與習俗相矛盾時：「命名它、慶祝它、建立在它上面」

---

### OpenSpec — 「行動前達成共識」

> "OpenSpec adds a lightweight spec layer before any code is written, ensuring humans and AI agree on what's being built."

四大原則：
- `fluid not rigid` — 無階段門控，依賴是啟用器而非鎖門
- `iterative not waterfall` — 邊學邊建
- `easy not complex` — 輕量設置
- `built for brownfield` — 為修改現有代碼優化，非僅新建

---

### Matt Pocock Skills — 「工程書籍的 Skill 化」

每個 skill 是將《Pragmatic Programmer》《DDD》《A Philosophy of Software Design》的最佳實踐**編碼為代理可執行的工作流**。

設計原則：
- Skill 不是「AI 能做什麼」，而是「好的工程實踐應該是什麼」
- 軟/硬依賴二分：新手零配置可用（軟依賴），進階用戶配置後獲完整功能（硬依賴）

---

### Superpowers — 「強制性不可逃避的檢查點」

```
<EXTREMELY-IMPORTANT>
IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.
This is not negotiable. This is not optional.
</EXTREMELY-IMPORTANT>
```

核心原則：
- `Test-Driven Development` — 測試優先，永遠
- `Systematic over ad-hoc` — 流程 > 猜測
- `Evidence over claims` — 驗證後才宣稱成功

---

## 三、設計亮點深度提取

### 亮點 1：Skill Description 的精密設計

**出處**：Matt Pocock Skills + Superpowers（兩者均獨立得出相同結論）

**問題**：description 是 agent 決定是否載入 skill 的**唯一依據**，設計不當會導致：
- 誤觸發（description 太寬泛）
- 漏觸發（沒有 "Use when" clause）
- 代理讀完 description 就停止，不讀主體（description 摘要了流程）

**Superpowers 的實驗（明確記錄在 `skills/writing-skills/SKILL.md`）**：
> 一個描述「two-stage review」的 description 導致代理只做了一次審查，儘管 skill 主體的 flowchart 清晰顯示了兩個階段。修改 description 只描述觸發條件後，代理正確讀完整 skill。

**規則**：
```yaml
# ❌ 摘要流程（導致代理跳過主體）
description: "Two-stage review: spec compliance then code quality"

# ✅ 只描述觸發條件
description: "Use when executing implementation plans with independent tasks"
```

**Matt Pocock 的 1024 字符限制模板**：
```
第一句：功能定義
第二句：Use when [關鍵詞觸發條件]
```

**可借鑒程度**：⭐⭐⭐⭐⭐ 直接影響 skill 是否被正確觸發

---

### 亮點 2：模板驅動的 Skill 代碼生成

**出處**：gstack（最完整實現）

**問題**：手寫 SKILL.md 時，文檔與實際代碼漂移（命令被移除、標誌被重命名，但文檔未更新）。

**解決方案**：
```
SKILL.md.tmpl（人類寫散文 + {{PLACEHOLDERS}}）
    ↓ bun run gen:skill-docs
    ↓ 從源代碼讀取元數據
SKILL.md（提交，部分自動生成）
```

占位符映射示例：
| 占位符 | 來源 | 生成內容 |
|--------|------|---------|
| `{{COMMAND_REFERENCE}}` | `commands.ts` | 分類命令表 |
| `{{SNAPSHOT_FLAGS}}` | `snapshot.ts` | 標誌參考 + 示例 |
| `{{PREAMBLE}}` | `gen-skill-docs.ts` | 啟動塊（更新檢查、session tracking） |

**進一步**：同一份 `.tmpl` 支持 10 個 AI agent 平台的輸出（Claude Code、Codex、Cursor、Factory 等），每個主機有不同的工具名稱、路徑、格式。

**可借鑒程度**：⭐⭐⭐⭐ 對當前規模可先用「sections」代替占位符；規模大後升級為模板系統

---

### 亮點 3：顯式工件鏈（Artifact Chain）

**出處**：gstack（最系統）+ OpenSpec（形式化為 DAG）

**問題**：代理完成一項工作後，下一個代理無法找到上下文（信息在對話歷史中，不在磁碟上）。

**gstack 的工件鏈設計**：

| Skill | 讀取 | 輸出 |
|-------|------|------|
| `/office-hours` | — | `PROJECT_PLAN.md` |
| `/plan-ceo-review` | `PROJECT_PLAN.md` | `PLAN_DECISIONS.md` |
| `/plan-eng-review` | `PLAN_DECISIONS.md` | `TEST_MATRIX.md` + 架構圖 |
| `/review` | `TEST_MATRIX.md` + `git diff` | 審查報告 + 修復提交 |
| `/qa` | 迴歸測試 | bug 修復 |
| `/ship` | 所有前述 | PR + 部署 |

**OpenSpec 的 DAG 形式化**：
```typescript
// 依賴是「啟用器」，不是「門」
graph.getNextArtifacts(completed)   // 「下一步能做什麼？」
graph.getBuildOrder()               // 拓撲排序
graph.getBlockedArtifacts()         // 被阻止的工件及原因
```

**與我們現有系統的關係**：我們的 `HANDOFF.md` 已有此思想，但工件路徑不夠顯式。每個 skill 應在 `<supporting-info>` 中明確列出：讀什麼文件、寫什麼文件。

**可借鑒程度**：⭐⭐⭐⭐⭐ 直接解決跨 stage 信息喪失問題

---

### 亮點 4：增量規格（Delta Specs）

**出處**：OpenSpec（獨有設計）

**問題**：修改現有系統時，只需描述「什麼改變了」，不應重寫整個規格。

**格式**：
```markdown
## ADDED Requirements
### Requirement: Two-Factor Authentication
The system MUST support TOTP-based two-factor authentication.

## MODIFIED Requirements
### Requirement: Session Expiration
The system MUST expire sessions after 15 minutes.
(Previously: 30 minutes)

## REMOVED Requirements
### Requirement: Remember Me
(Deprecated in favor of 2FA)
```

**歸檔時的合併**：
- `ADDED` → 附加到主規格
- `MODIFIED` → 替換現有需求（按 ID 定位）
- `REMOVED` → 從主規格刪除

**優勢**：
1. **棕田支持** — 明確標示「之前是什麼，現在改為什麼」
2. **無衝突** — 多人協作時各自編輯不同需求 ID
3. **PR 清晰** — Code review 只看差異

**可借鑒程度**：⭐⭐⭐⭐ 我們的 `s2-struct-req` 可考慮引入 `MODIFIED` 標記

---

### 亮點 5：紅旗表（Red Flags Table）

**出處**：Superpowers + Matt Pocock Skills（各自獨立實現）

**問題**：代理會「rationalize」（理性化）逃避 skill：「太簡單了，不需要 skill」「我先弄清楚上下文再說」。

**解決方案**：每個 skill 內嵌「您不應該有的想法」表格：

```markdown
## Red Flags — Stop and Start Over

| 想法 | 現實 |
|------|------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I already manually tested it" | Ad-hoc ≠ systematic. No record. Can't rerun. |
```

**已在我們系統中應用**：`s4-tdd/SKILL.md` 已有「Common Rationalizations」表格，`s0-trace-feature/SKILL.md` 已有「Red Flags — Stop and Read the Source」（本輪改進中加入）。

**擴展機會**：`s3-eval-system`、`s5-pr-review`、`s6-verify-release` 可加入對應的紅旗表。

**可借鑒程度**：⭐⭐⭐⭐⭐ 簡單且高效的 anti-rationalization 機制

---

### 亮點 6：Domain-Driven Documentation 作為 AI 詞彙表

**出處**：Matt Pocock Skills（最系統化）

**問題**：agent 需反復推理「account 是指 Customer 還是 User？」浪費令牌，且推理結果不一致。

**解決方案**：`CONTEXT.md` 是寫給 AI 的詞彙表（非人用文檔）：

```markdown
# CONTEXT.md 示例

**Order**:
A request by a customer for goods or services.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

## Relationships
- An **Order** produces one or more **Invoices**

## Flagged ambiguities
- "account" was used to mean both Customer and User — resolved: these are distinct.
```

**ADR 三層檢查**（`docs/adr/ADR-FORMAT.md`）：
- Hard to reverse？
- Surprising to a new reader？
- Trade-off involved？
若三者均否，無需寫 ADR（防止過度文檔化）。

**令牌影響**：-20-30%（代理不需重複推理術語）

**可借鑒程度**：⭐⭐⭐⭐ 我們的 `CONTEXT.md` 已有此結構，可加入 `_Avoid_` 標記和 `Flagged ambiguities` 部分

---

### 亮點 7：AI Skill 的集成測試框架

**出處**：Superpowers（業界罕見）

**問題**：如何驗證 skill 真的產生了預期行為？單元測試無法捕捉代理行為。

**解決方案**：解析 Claude Code 會話的 `.jsonl` 記錄：

```bash
# 驗證 skill 是否被調用
grep -q '"name":"Skill".*"skill":"subagent-driven-development"' "$SESSION_FILE"

# 驗證子代理被分派
grep '"type":"user"' "$SESSION_FILE" | grep '"agentId"' | wc -l

# 令牌分析
python3 analyze-token-usage.py "$SESSION_FILE"
```

**8 項集成測試驗證清單**：
1. Skill 工具被調用
2. 子代理被正確分派
3. 任務追蹤工具使用
4. 實施文件正確生成
5. 測試通過
6. 無額外功能被添加
7. Git commits 顯示正確工作流
8. 代碼審查通過

**可借鑒程度**：⭐⭐⭐ 對我們系統驗證 skill 行為有高價值，但成本高（每次測試 10-30 分鐘）

---

### 亮點 8：Schema 驅動的工作流配置

**出處**：OpenSpec（最形式化）

**問題**：工作流硬編碼在 TypeScript 中，修改需重新構建；無法讓團隊自定義。

**解決方案**：工作流定義在 YAML 中：

```yaml
# schemas/spec-driven/schema.yaml
name: spec-driven
artifacts:
  - id: proposal
    generates: proposal.md
    requires: []
    instruction: |
      Create the proposal document...
  
  - id: specs
    generates: specs/**/*.md
    requires: [proposal]
    instruction: |
      Create specification files...
```

**上下文注入**：`openspec/config.yaml` 為 AI 提供項目特定上下文：

```yaml
context: |
  Tech stack: TypeScript, React, Node.js (≥20.19.0)
  Package manager: pnpm

rules:
  specs:
    - Include scenarios for Windows path handling
  tasks:
    - Add Windows CI verification
```

**可借鑒程度**：⭐⭐⭐ 對我們的 `RULES.md + CONTEXT.md` 體系是增強，可考慮在 `CONTEXT_SNAPSHOT.md` 中加入 `rules` 分節

---

### 亮點 9：工具無關的命令適配器模式

**出處**：OpenSpec（最系統）+ gstack（多主機生成）

**問題**：同一套工作流邏輯需要在 Claude Code、Cursor、Copilot、Gemini 等不同平台運行。

**OpenSpec 的 Adapter Pattern**：
```
CommandContent（工具無關）
        ↓
├─► ClaudeSkillAdapter    → .claude/skills/openspec-*/SKILL.md
├─► CursorRulesAdapter    → .cursor/rules/openspec.md
├─► GitHubCopilotAdapter  → .github/copilot-instructions.md
└─► WindsurfAdapter       → configurable
```

**Superpowers 的環境檢測方案**（輕量版）：
```bash
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
  output_cursor_format
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  output_claude_format
else
  output_sdk_standard
fi
```

**可借鑒程度**：⭐⭐⭐ 目前我們主要針對 Claude Code，但架構上可預留多平台支持點

---

### 亮點 10：守護進程 + 持久狀態模型

**出處**：gstack（解決瀏覽器自動化的特殊問題）

**問題**：每次 MCP 工具調用重啟瀏覽器需 3-5 秒，無法跨調用持久化 session 狀態。

**解決方案**：
```
CLI（Bun 編譯二進制）
    ↓ HTTP POST /command
Bun.serve() HTTP 服務器
    ↓ CDP
Chromium 守護進程（30 分鐘空閒超時）
```

效果：首次 ~3 秒，後續 ~100-200ms（10-30× 加速）。

**安全設計**：物理端口分離（本地完整表面 vs. 隧道有限表面），而非依賴頭部過濾。

**可借鑒程度**：⭐⭐ 對當前系統直接應用有限，但「狀態持久化 > 每次冷啟動」的思想可用於 CI 環境優化

---

## 四、交叉主題：各倉庫的共同洞察

這四個完全獨立開發的倉庫，在以下幾個點上不約而同地得出了相同結論：

### 主題 1：輸出紀律（Output Discipline）

所有四個倉庫都強調：**代理必須停止並等待人類顯式批准，才能繼續。**

- gstack：`AskUserQuestion` 統一格式：context → question → `RECOMMENDATION: Choose X because ___` → lettered options
- superpowers：`<HARD-GATE>` + EXTREMELY IMPORTANT 強制語言
- Matt Pocock：硬/軟依賴二分，硬依賴需顯式 setup
- OpenSpec：工件 DAG 讓「下一步能做什麼」透明可查

**我們的系統已實現**：每個 skill 的 `<HARD-GATE>` + "Awaiting your approval" 尾句。

### 主題 2：Evidence over Assertion（證據優於斷言）

- gstack：「It worked when I tried it is not evidence. Automated test results are evidence.」
- superpowers：集成測試驗證 8 項（不只是「我說它通過了」）
- Matt Pocock：「Watch the test FAIL before writing production code」
- OpenSpec：`openspec validate` 命令 + `openspec status --json` 可查

**我們的系統已實現**：`s4-tdd` 要求貼終端輸出，`s6-verify-release` 要求機器生成 `test-results.json`。

### 主題 3：Skill 即工程文化的外部化

四個倉庫都不是「prompt 集合」，而是把**軟體工程最佳實踐編碼為代理可執行的強制流程**：
- TDD、代碼審查、部署流程、除錯方法論 → 都以 skill 形式存在
- Skill 告訴代理「要做什麼」比 CLAUDE.md 的通用指南更強制

### 主題 4：設計 for AI 的文檔，而非設計 for 人類的文檔

- CONTEXT.md、ADRs、config rules 都是明確寫給 AI 看的
- 包含 `_Avoid_` 字段、`"Use when"` 子句、觸發關鍵詞列表
- 人類也能讀，但格式是為 AI 解析優化的

---

## 五、對本系統的具體改進建議

基於以上分析，以下是按優先級排序的改進機會：

### P1 — 高優先級（影響大、實施容易）

**P1.1 — 在高風險 skill 加入工件讀寫聲明**

在每個 skill 的 `<supporting-info>` 的 Artifact Standard 部分，明確列出：
```markdown
## Artifact Standard
- **Reads**: `docs/specs/YYYY-MM-DD-<topic>-requirements.md`, `CONTEXT_SNAPSHOT.md`
- **Writes**: `docs/arch/YYYY-MM-DD-<topic>-impact.md`
- **Must commit before**: transitioning to `/s3-design-arch`
```

影響：解決跨 stage 信息喪失，代理知道去哪找上下文。

---

**P1.2 — 為缺少紅旗表的高風險 skill 補充 Red Flags**

目前已有：`s4-tdd`（Common Rationalizations）、`s0-trace-feature`（Red Flags）

建議補充：
- `s3-eval-system` — 添加「跳過 Step 1b 直接掃描」類的紅旗
- `s5-pr-review` — 添加「通過了就算通過」類的紅旗
- `s6-verify-release` — 添加「coverage 接近門檻就算通過」類的紅旗

---

**P1.3 — 優化 CONTEXT.md 的 AI 可讀性**

借鑒 Matt Pocock 格式，為每個術語加入：
```markdown
**Atomic Task**:
A unit of work completable in ≤5 minutes by one implementer.
_Avoid_: task, story, ticket, item

**HARD-GATE**:
A mandatory blocking check in a skill that prevents the agent from proceeding.
_Avoid_: checkpoint, gate, blocker (ambiguous)

## Flagged ambiguities
- "stage" was used to mean both the numbered SDLC phase AND a deployment environment — resolved: "Stage N" is always SDLC; "environment" is deployment.
```

---

### P2 — 中優先級（影響中等、需要更多設計）

**P2.1 — 為 `s2-struct-req` 引入 Delta Spec 格式**

當進行功能迭代時，需求文件應支持增量標記：
```markdown
## MODIFIED Requirements
### REQ-3: Session Expiration (Modified)
The system MUST expire sessions after **15 minutes**.
(Previously: 30 minutes — changed per security audit 2026-05)
```

---

**P2.2 — 在 `CONTEXT_SNAPSHOT.md` 加入 `rules` 分節**

借鑒 OpenSpec 的 `config.yaml` 上下文注入：
```markdown
## Agent Rules for This Iteration

### For s3-eval-system
- Flag any file exceeding 400 lines as a blocker
- Treat all auth-related changes as 🔴 BREAKING

### For s4-tdd
- Test file naming: `test_*.py` (pytest convention)
- All DB calls must use `pytest-django`'s `@pytest.mark.django_db`
```

---

**P2.3 — 建立 Skill 端對端測試框架（輕量版）**

借鑒 Superpowers，不需要完整實現，先從一個 skill 開始：
```bash
# test-s4-tdd.sh
PROMPT="Add a function that multiplies two numbers. Use TDD."
claude -p "$PROMPT" --allowed-tools=all --add-dir "$TEST_PROJECT"

SESSION_FILE=$(find ~/.claude/projects -name "*.jsonl" -mmin -10 | head -1)

# 驗證：TDD 流程是否被遵循
grep -q '"name":"Skill".*"skill":"s4-tdd"' "$SESSION_FILE" && echo "[PASS] Skill invoked"
grep -q '"name":"Bash".*"pytest.*FAILED"' "$SESSION_FILE" && echo "[PASS] Watched test fail"
```

---

### P3 — 低優先級（長期規劃）

**P3.1 — 模板系統（SKILL.md.tmpl）**

當 skill 數量 > 40 個後，考慮引入模板系統，讓命令參考從代碼自動生成。

**P3.2 — 多平台支持**

為 Cursor、Copilot 用戶提供工具映射表（`docs/tool-mappings/cursor.md`），讓 skill 內容不需改動即可跨平台使用。

---

## 六、設計品質評分對比

| 維度 | gstack | OpenSpec | Matt Pocock | Superpowers | 本系統 |
|------|--------|---------|-------------|------------|-------|
| Skill 描述精密度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 工件鏈顯式化 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 強制執行機制 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 輸入質量保護 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 多平台支持 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| 測試/驗證框架 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 棕田支持 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

**本系統最強項**：強制執行機制（HARD-GATE + 輸出紀律），與 Superpowers 同級。
**本系統最大機會**：工件鏈顯式化 + 多平台支持。

---

## 七、結語

四個倉庫代表了 AI Agentic 工具設計的四個不同切角：

- **gstack** — 工程生產力的最大化（速度 × 輸出量）
- **OpenSpec** — 人機共識的形式化（規格 × 工件依賴）
- **Matt Pocock** — 工程文化的外部化（認知流程 → skill）
- **Superpowers** — 強制執行的系統化（不可逃避 × 可驗證）

本系統（Agentic SDLC Skills）的定位是：**完整 SDLC 流程的強制執行**，這是四個倉庫中都沒有完整覆蓋的維度。它的核心優勢是端對端的 7 stage 流程 + HARD-GATE 機制，與上述倉庫是互補而非替代關係。

最值得立即借鑒的三點：
1. **Skill Description 只描述觸發條件**（Superpowers + Matt Pocock 實驗驗證）
2. **在每個 skill 明確聲明讀什麼/寫什麼工件**（gstack + OpenSpec 共同洞察）
3. **為每個高風險 skill 補充 Red Flags 表**（Superpowers + Matt Pocock 共同設計）