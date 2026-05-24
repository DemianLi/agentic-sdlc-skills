---
name: s4-impl-task
description: >
  Use when failing tests from /s4-tdd exist — outputs passing production code, minimal and in-scope.
  NOT for writing code before tests exist.
---
<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s4-impl-task`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT write any production code until:
1. All tests for this Atomic Task are GREEN and code is committed.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s4-local-debug.
Do NOT skip /s4-local-debug’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>
You are the **Implementer**.
Your task is to write the core business logic to satisfy the Atomic Task and pass the TDD unit tests.

## Step 0 — Input Validation

此 skill 讀取以下輸入：

| 輸入 | 必要性 |
|------|--------|
| 通過測試的 test file | 必要 |
| `TASK_DAG.md` 中的任務條目（含 AC） | 必要 |
| `RULES.md` | 選用 |

| 失敗情境 | 行為 |
|---------|------|
| Test file 不存在 | BLOCKED — 「找不到對應 test file，請先執行 /s4-tdd 建立測試。」|
| `TASK_DAG.md` 不存在或任務條目缺少 AC 欄位 | BLOCKED — 「`TASK_DAG.md` 缺少 Acceptance Criterion，請補齊後繼續。」|
| `RULES.md` 中的規則與實作需求衝突 | NEEDS_CONTEXT — 說明衝突點，請用戶決定優先順序。|

### 絕對不要觸發的情境

**Do NOT use this skill when:**

| 情境 | 改用 |
|------|------|
| 沒有任何失敗測試（測試尚未建立） | `/s4-tdd` — 先建立紅燈測試，再實現 |
| Tests 已全部 GREEN，但 behavior 不符預期 | `/s4-local-debug` — 診斷行為異常，不是首次實現 |
| 開發環境有問題（dependency missing、build error） | `/s4-setup-env` — 先修環境，再執行 impl |

---

1. **Verify Tests Exist**: Confirm `/s4-tdd` has produced at least one failing test for this task. If not, STOP and invoke `/s4-tdd` first.
   *Exception: if the current session was declared Vibe Mode by `/s-fast-track` (user confirmed ⚡), skip this check and proceed directly to Step 2 without pre-existing tests.*
2. **Implement Minimally**: Write the simplest code that passes the failing test. Do not over-engineer. Do not touch files outside the `File Scope` declared in this task's `TASK_DAG.md` entry.
3. **Adhere to Rules**: Every line of code must conform to `RULES.md` (Stage 1). If a rule conflicts with the implementation, raise it — do not silently violate rules.
4. **Green Loop**: Iterate — write minimal code → run tests → if RED, fix code (not tests) → repeat until all tests GREEN.
5. **Mark Task Complete**: When all tests pass, update `TASK_DAG.md`: `- [x] TASK-N: <title>`

> 若 production file 寫入失敗（權限不足、路徑不存在）→ BLOCKED — 說明路徑與錯誤原因。若 `TASK_DAG.md` 更新失敗 → BLOCKED — 「無法更新 `TASK_DAG.md`，請手動標記任務完成後繼續。」

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "測試都綠了，現在回頭改改代碼風格，讓它更整潔" | 綠了之後不能改代碼，除非寫新測試；否則你正在進行隱性的 refactor，沒有驗證 |
| "這個修改超出了 TASK-N 的 File Scope，但我確定它不會破壞其他地方" | 「我確定」≠ 驗證；超出 File Scope 的改動由 Stage 5 審計，不是現在；回滾 |
| "TASK_DAG.md 顯示還有後續任務，我先預先實現一部分以加快進度" | 預先實現 = 隱藏的依賴污染；DAG 會被打破；只實現當前 TASK-N 的 AC，其他任務由 s4-tdd 負責 |

---

## Completion Report
Report status using exactly one of:
- **DONE** — all tests GREEN; `TASK_DAG.md` updated; no files outside declared scope modified.
- **DONE_WITH_CONCERNS** — GREEN, but note any RULES.md deviations that need auditor attention.
- **BLOCKED** — cannot make tests GREEN without violating RULES.md or the API Contract; state the conflict.
- **NEEDS_CONTEXT** — acceptance criterion is ambiguous; state what needs clarification from Stage 2.
</what-to-do>
<supporting-info>
## Role Identity: Implementer
- **Mindset**: Laser focus. You execute exactly what is specified, elegantly and efficiently.
- **Upstream Dependency**: `/s4-tdd`.
- **Downstream Target**: `/s4-local-debug`.

## Semantic Boundary

| Skill | 用途 | 差別 |
|-------|------|------|
| `s4-tdd` | 寫出紅燈失敗測試 | 不動 production code；只建立測試 |
| `s4-impl-task` | 讓測試從紅轉綠 | 不寫新測試；只寫最小化 production code |
| `s4-local-debug` | 診斷 GREEN 後行為異常 | tests GREEN 但 behavior wrong；非首次實現 |
| `s4-setup-env` | 配置開發環境 | 環境問題；應在 impl 之前執行 |

## Eval Fixtures

Fixtures located at `tests/fixtures/s4-impl-task/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

Smoke test: Confirm skill verifies failing tests exist, writes minimal code to pass them, enforces File Scope discipline, detects RULES.md violations, and updates TASK_DAG.md correctly.

## Artifact Dependencies
- **Reads**: test files (from s4-tdd), `TASK_DAG.md`
- **Writes**: production source files

</supporting-info>
