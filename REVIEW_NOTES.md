# Skill Generation & Review Tracker

## Review Process
This document tracks the status of all 27 atomic skills across the 7 stages of the Agentic SDLC. 
Please use this document to record any review feedback or required modifications for the generated skills.

### Stage 1: Foundation Engineer
- [x] `/s1-define-rules`
- [x] `/s1-config-context`
- [x] `/s1-lock-tech-stack`

### Stage 2: Product Manager
- [x] `/s2-capture-vision`
- [x] `/s2-align-req`
- [x] `/s2-struct-req`
- [x] `/s2-snapshot-ctx`

### Stage 3: System Architect
- [x] `/s3-eval-system`
- [x] `/s3-design-arch`
- [x] `/s3-breakdown-wbs`
- [x] `/s3-build-dag`

### Stage 4: Implementer
- [x] `/s4-setup-env`
- [x] `/s4-impl-task`
- [x] `/s4-tdd`
- [x] `/s4-local-debug`

### Stage 5: Code Auditor
- [x] `/s5-sast-lint`
- [x] `/s5-audit-rules`
- [x] `/s5-pr-review`
- [x] `/s5-fix-optimize`

### Stage 6: QA Engineer
- [x] `/s6-test-integration`
- [x] `/s6-test-e2e`
- [x] `/s6-test-perf`
- [x] `/s6-verify-release`

### Stage 7: Release Manager
- [x] `/s7-build-artifact`
- [x] `/s7-release-notes`
- [x] `/s7-deploy`
- [x] `/s7-telemetry`

---

## 📝 深度審查反饋 — 基於四大倉庫第一手源碼分析
*(Review grounded in real source code from the four repositories)*

> **審查方法論**: 本次反饋直接對照四大倉庫的原始 SKILL.md 文件進行比對，找出我們的 27 個 Skill 與黃金標準之間的差距。

---

### 🔴 全局問題 (Critical — 所有 27 個 Skill 均受影響)

#### 問題 1：缺少 `<HARD-GATE>` 防止 Agent 暴走 (源自 superpowers/brainstorming)

**原始証據** — `superpowers/brainstorming/SKILL.md` 採用了明確的阻斷語法：
```xml
<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or
take any implementation action until you have presented a design and the user
has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>
```
**我們的問題**: 我們的 Skill 完全沒有任何 `<HARD-GATE>` 或等效的強制暫停機制，Agent 可以一路從 s1 執行到 s7 而不徵求使用者同意。

**修改方向**: 在每個 Skill 的 `<what-to-do>` 開頭加入明確的 STOP 條件，例如：
```xml
<HARD-GATE>
Do NOT proceed to the next step until you have presented the artifact and received
explicit user approval. Use a checklist item to mark when approval is granted.
</HARD-GATE>
```

---

#### 問題 2：缺少 Dot-Graph 流程圖，步驟順序不可驗證 (源自 superpowers/brainstorming)

**原始証據** — `superpowers/brainstorming/SKILL.md` 使用了 Graphviz Dot 語法定義可機器解析的 DAG：
```dot
digraph brainstorming {
    "Explore project context" -> "Visual questions ahead?";
    "User approves design?" -> "Write design doc" [label="yes"];
    "User approves design?" -> "Present design sections" [label="no, revise"];
    ...
    "Invoke writing-plans skill" [shape=doublecircle];
}
```
**我們的問題**: 我們的步驟列表是純文字，Agent 無法機器驗證 DAG 的拓撲正確性。終止狀態（`doublecircle`）也未標示。

**修改方向**: 所有 Stage 3+ 的複雜 Skill 應加入 `## Process Flow` 節點，使用 Dot 語法定義入口、決策點與終止狀態。

---

#### 問題 3：缺少 Vertical Slice TDD，水平分割反模式 (源自 mattpocock/tdd)

**原始証據** — `mattpocock/skills/tdd/SKILL.md` 明確定義了「橫向切割反模式」：
```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
```
**我們的問題**: `s4-tdd` 和 `s4-impl-task` 沒有明確禁止水平切割，Agent 極可能一次寫所有測試再寫所有代碼。

---

#### 問題 4：缺少完整的 Completion Status Protocol (源自 gstack/review)

**原始証據** — gstack 的每個 Skill 結尾都有標準化的完成報告：
```markdown
## Completion Status Protocol
- **DONE** — completed with evidence.
- **DONE_WITH_CONCERNS** — completed, but list concerns.
- **BLOCKED** — cannot proceed; state blocker and what was tried.
- **NEEDS_CONTEXT** — missing info; state exactly what is needed.
```
**我們的問題**: 我們的 Skill 沒有定義 Agent 如何回報執行結果，導致用戶不知道 Agent 是真的完成了還是卡住了。

---

### 🟡 分階段反饋 (Per-Stage Issues)

#### Stage 1 — Foundation Engineer ✅ 整體良好，微調即可

**優點**: `s1-define-rules` 的 Artifact Standard 定義了 `RULES.md` 的三個必要章節（Linter、Directory、Forbidden），是所有 Skill 中最完整的。

**待改進**:
- `s1-config-context` 應對齊 `mattpocock/grill-with-docs` 的 CONTEXT.md 格式規範：
  > *"CONTEXT.md should be totally devoid of implementation details. It is a glossary and nothing else."*
  - 需加入：**何時** 更新 (`update CONTEXT.md inline, don't batch these up`)
  - 需加入：**ADR 的三個觸發條件**（Hard to reverse / Surprising without context / Real trade-off）

---

#### Stage 2 — Product Manager 🔴 需要大幅重構

**問題**: `s2-capture-vision` 目前只有 13 行，遠低於 superpowers `brainstorming` 的 161 行標準。

**具體缺失**:
1. **沒有「作用域過大時的分解策略」**: superpowers 明確說明：若需求涉及多個獨立子系統，應先分解為子項目，各自有獨立的 spec → plan → implementation 循環。
2. **沒有多方案比較**: superpowers 要求 `Propose 2-3 approaches with trade-offs and your recommendation`。
3. **Artifact Standard 缺失**: `s2-struct-req` 沒有定義需求文件的格式，應輸出到 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`。
4. **Spec Self-Review 機制缺失**: 寫完 spec 後需要自我審查（Placeholder scan / Internal consistency / Scope check / Ambiguity check）。

---

#### Stage 3 — System Architect 🔴 缺少 OpenSpec 格式規範

**問題**: `s3-design-arch` 只有 20 行，沒有定義 Design Doc 的具體格式。

**修改方向 (對齊 Fission-AI/OpenSpec 精神)**:
- 要求輸出 OpenSpec 格式的設計文件，包含：
  - `## Context` — 背景與問題陳述
  - `## Decision` — 選擇的技術方案
  - `## Consequences` — 已知的權衡取捨
  - Mermaid 序列圖（Sequence Diagram）作為必要附件
- `s3-build-dag` 應明確要求使用 Graphviz Dot 或 Mermaid 語法輸出任務依賴圖，且每個任務節點需標明 **預估時間**（2-5 分鐘原則，來自 superpowers/writing-plans）

---

#### Stage 4 — Implementer 🔴 TDD 強度不足

**問題**: `s4-tdd` 缺少「鐵律」宣告與反模式說明。

**修改方向 (對齊 superpowers/test-driven-development)**:

需加入 **The Iron Law** 節：
```markdown
## The Iron Law
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

Write code before the test? Delete it. Start over.
- Don't keep it as "reference"
- Delete means delete
```

需加入 **Common Rationalizations** 章節（處理 Agent 可能的「合理化」藉口）：
| 藉口 | 現實 |
|------|------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |

**`s4-local-debug` 修改方向 (對齊 mattpocock/diagnose)**:
需加入 `reproduce → minimise → hypothesise → instrument → fix → regression-test` 的六步驟診斷循環。

---

#### Stage 5 — Code Auditor 🟡 缺少 gstack Voice 規範

**問題**: `s5-pr-review` 沒有定義 Code Review 的輸出格式與嚴重性分級。

**修改方向 (對齊 gstack/review)**:
- 加入 **Scope Drift Detection**（對比 stated intent vs. actual diff，防止 Agent 做超出範疇的修改）
- 加入問題嚴重性分級：`CRITICAL` / `WARNING` / `SUGGESTION`
- 加入 **完成報告格式**（引用 gstack 的 Completion Status Protocol）

gstack 的 `Voice` 規範也值得引入，讓 Agent 的審查報告更具工程師風格：
> *"Be concrete. Name files, functions, line numbers, commands, outputs."*

---

#### Stage 6 — QA Engineer 🟡 缺少覆蓋率門檻

**問題**: `s6-test-integration` 和 `s6-test-e2e` 沒有定義量化的品質門檻。

**修改方向**:
- 加入明確的覆蓋率要求：`Unit tests: 80%+ / Integration: Critical paths / E2E: Main user flows`
- `s6-verify-release` 的 Artifact Standard 應輸出 `test-results.json`，包含：
  ```json
  {
    "coverage": 85.3,
    "total_tests": 142,
    "passed": 140,
    "failed": 2,
    "release_gate": "BLOCKED"
  }
  ```
- 加入 **Verification Before Completion** 機制（superpowers 強調：「If you didn't watch the test fail, you don't know if it tests the right thing.」）

---

#### Stage 7 — Release Manager 🟡 缺少 Telemetry 與 Canary 機制

**問題**: `s7-deploy` 和 `s7-telemetry` 沒有定義部署後的健康檢查流程。

**修改方向 (對齊 gstack/canary + gstack/land-and-deploy)**:
- `s7-deploy` 應包含三階段：`deploy → monitor → verify`
- `s7-telemetry` 應輸出結構化的部署報告（Skill Completion Report），包含：
  - 部署時間戳
  - 關鍵指標基線（Latency P99 / Error Rate / Saturation）
  - Rollback 觸發條件（明確的數值門檻）
- `s7-release-notes` 應定義 CHANGELOG 格式（遵循 Keep a Changelog 規範）

---

### 📋 下一步行動優先順序

| 優先級 | 行動 | 影響範圍 |
|--------|------|---------|
| 🔴 P0 | 為所有 Skill 加入 `<HARD-GATE>` 暫停機制 | 27 個 Skill |
| 🔴 P0 | 為 `s4-tdd` 加入 Iron Law + 垂直切片要求 | s4-tdd |
| 🔴 P1 | 大幅重構 `s2-capture-vision`，對齊 superpowers brainstorming 的 9 步驟 checklist | s2-* |
| 🟡 P1 | 為 `s3-design-arch` 定義 OpenSpec 輸出格式與 Mermaid 要求 | s3-* |
| 🟡 P2 | 為 `s5-pr-review` 加入 Scope Drift Detection 與嚴重性分級 | s5-* |
| 🟡 P2 | 為 `s6-verify-release` 定義量化的品質門檻與 JSON 報告格式 | s6-* |
| 🟢 P3 | 為 `s7-deploy` 加入 Canary 監控與 Rollback 觸發條件 | s7-* |
