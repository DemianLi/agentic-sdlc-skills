# ADR-0002: Dynamic Damper — 三檔開發模式系統

**Status:** Accepted  
**Date:** 2026-05-18  
**Deciders:** @demian  

---

## Context

### 現有架構的問題

目前 Agentic SDLC Skills 系統有兩個入口：

| 入口 | 跳過的 Gates | 保留的 Gates |
|------|-------------|-------------|
| `s1` 全量流程 | 無 | G1~G4 全部開啟 |
| `s-fast-track` | s1~s3 ceremony | s4 TDD Iron Law 保留 |

這解決了「大型專案 vs 小型原子任務」的分流，但留下了兩個未解決的問題：

1. **下游 s5+ 不知道模式** — `s-fast-track` 讓使用者快速抵達 s4，但 s5-pr-review、s5-sast-lint、s5-audit-rules 在 hotfix 場景下的嚴格度與 greenfield 完全相同，仍然造成認知摩擦。

2. **沒有明確的豁免宣告機制** — 使用者想進入「探索/原型」模式時，必須仰賴 `s-fast-track` 把任務描述分類為 `Exploratory prototype` 才能被路由到 `s4-impl-task`（TDD optional）。沒有明確旗標，AI 有可能錯誤分類並套用 TDD Iron Law。

### 已存在但未被明確化的行為

`s-fast-track` 現有路由表已有這一行（但沒有明確旗標觸發）：
> `Exploratory prototype (throwaway)` → `/s4-impl-task` — *TDD optional*

這意味著「Vibe Mode 豁免 TDD Iron Law」在行為上已部分成立，只缺乏顯式宣告。

---

## Decision Drivers

1. **防止「狼來了」效應**：在任何微小修改都跳 HARD-GATE 警告，開發者會進入「盲目批准」模式，讓所有安全網形同虛設。
2. **不增加新的技術債界面**：任何豁免都必須留下可追溯的記錄（commit tag、對話確認）。
3. **Iron Law 的核心不能動**：TDD Iron Law 是防止 AI 悄悄寫無測試生產代碼的最後防線。任何模式都不能「靜默跳過」它，但可以「顯式豁免」它。
4. **外科手術式修改**：優先擴展現有 `s-fast-track`，而非打造新技能或新 dispatcher。

---

## Options Considered

### Option A：CLI 旗標 + `s-fast-track` 延伸（**推薦**）

在 `s-fast-track` 加入對 intent signal 的識別：使用者可以在任務描述末尾加上 `--vibe` 或 `--hotfix`，或用自然語言表達「這是探索性/hotfix」。

- `--vibe` / "just exploring" / "throwaway script"  
  → 路由到 `s4-impl-task`（TDD optional）  
  → commit message 必須加 `[WIP/Prototype]` 標籤  
  → s5 下游全部跳過（不進入 PR review 流程）

- `--hotfix` / "quick fix" / "on a legacy project"  
  → 路由到 `s4-tdd`（TDD 保留）  
  → s5-pr-review 進入「精簡模式」：只審 CRITICAL，跳過 STYLE/MINOR  
  → 允許在沒有完整 `test-results.json` 的情況下合併（需使用者明確說 "LGTM, deploy"）

**優點：** 最小改動、意圖顯式、可追溯  
**缺點：** 開發者需要記住旗標語法（可用自然語言替代）

---

### Option B：s4-tdd 加入「豁免條款」段落

在 `s4-tdd/SKILL.md` 的 Red Flags 表格加入一行：
> 如果使用者明確說「Bypass TDD for prototype」→ 詢問確認 → 允許跳過，commit 加 `[WIP/Prototype]`

**優點：** 改動集中、Iron Law 的豁免路徑在 s4 本身就說清楚  
**缺點：** 修改了最核心的 Iron Law 文件，破壞其「無例外」的震懾力；如果模式判斷錯誤，AI 可能在不該豁免的時候豁免

---

### Option C：智慧路由 Dispatcher（s0-trace-feature 或新技能）

讓 s0 入口根據 blast radius 自動判斷模式，推薦合適的檔位。

**優點：** 自動化，使用者不需記旗標  
**缺點：** blast radius 的判斷本身需要 AI 的判斷力，容易誤判；加了一層複雜度；目前 `s-fast-track` 已提供 75% 的功能

---

## Decision

**採用 Option A**，具體改動如下：

### 改動 1：擴展 `s-fast-track/SKILL.md` — 加入旗標識別

在「Routing Table」前加入 intent signal 識別邏輯。

| 使用者描述中包含… | 觸發模式 | 路由行為 |
|---|---|---|
| `--vibe`、"just explore"、"throwaway"、"prototype" | **Vibe Mode** | → `s4-impl-task`（TDD optional）；強制 commit tag `[WIP/Prototype]` |
| `--hotfix`、"quick fix"、"legacy"、"no tests in this project" | **Hotfix Mode** | → `s4-tdd`（TDD 保留）；下游 s5 進入精簡審查 |
| 其他 | **Standard Fast-Track** | 現有行為不變 |

Vibe Mode 啟動時，必須對使用者打印確認：
```
⚡ Vibe Mode: TDD is optional. No s5 review.
   Commit MUST be tagged [WIP/Prototype].
   This creates tech debt. Confirm? (Y/n)
```

### 改動 2：在 `s5-pr-review/SKILL.md` 加入 Hotfix 精簡模式

在 HARD-GATE 條件前加入判斷：
> 若 session 中曾宣告 `--hotfix`，則：CRITICAL issues 仍為阻塞，但 STYLE/MINOR 自動降級為警告，允許繼續。

### 改動 3：不改動 `s4-tdd`

Iron Law 的「無例外」震懾力必須保留。Vibe Mode 通過路由到 `s4-impl-task` 來繞過它，而非修改它的文字。

---

## Consequences

### 正面影響

- 使用者可以在三種模式間顯式切換，而非猜測 AI 的路由決定
- Iron Law 的文字保持完整，不被豁免邏輯污染
- `[WIP/Prototype]` 標籤讓技術債在 git log 中可見可追蹤
- hotfix 場景的 s5 摩擦大幅降低，同時保留 CRITICAL 問題的阻塞力

### 負面影響 / 風險

- 開發者必須在任務描述中顯式宣告模式（若不宣告，行為與現在相同）
- Vibe Mode 的技術債需要後續清理（靠 `[WIP/Prototype]` tag 追蹤，不自動提醒）
- `--hotfix` 的「精簡 s5」依賴 AI 記憶 session 中的宣告，跨對話不持久

### 非目標（明確不做）

- 不建立獨立的 dispatcher 技能（複雜度 > 收益）
- 不弱化 TDD Iron Law 的文字
- 不讓 Vibe Mode 靜默跳過任何確認步驟（豁免必須顯式）

---

## 實作優先序

| 優先序 | 改動項目 | 估計複雜度 |
|---|---|---|
| P0 | 擴展 `s-fast-track` 加入旗標識別 + Vibe Mode 確認提示 | 低（~20 行） |
| P1 | `s5-pr-review` 加入 Hotfix 精簡模式邏輯 | 低（~10 行） |
| P2 | README / CONTEXT.md 加入三檔模式說明 | 低（文件更新） |
