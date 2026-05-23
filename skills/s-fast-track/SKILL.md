---
name: s-fast-track
description: >
  Use when task is a bug fix or brownfield feature add — outputs minimal RULES.md
  and routes to s4 implementation. NOT for greenfield projects needing full s1–s3.
---

<HARD-GATE>
⛔ MODE CONFIRMATION — do not proceed to s4 until the required interaction for the active mode is complete:

**Express Mode**（RULES.md 不存在）: print `"Express Mode: generating minimal artifacts (3 questions). Add --vibe to skip."` → 3-Question Interview → write artifacts → route.

**Standard Mode**（RULES.md 存在）: print `"Fast-track mode: RULES.md found — going directly to s4."` → ask ONE question → route.

**Vibe Mode**（`--vibe` flag）: print Vibe confirmation → wait for explicit Y → route. This is a second required gate.
</HARD-GATE>

<what-to-do>

You are the **Fast-Track Router**. Your only job is to skip the ceremony and get the user to s4 as fast as possible — without losing the engineering discipline that lives there.

## Step 0 — Input Validation

此 skill 接受唯一用戶輸入：**任務描述**（一句話）。

| 失敗情境 | 行為 |
|---------|------|
| 描述為空字串或僅空白 | Re-prompt：「請用一句話描述這個任務。」停止路由。|
| 描述超過三句或顯然模糊 | Re-prompt：「請濃縮成一句話：完成後什麼東西會壞掉，或什麼東西會存在？」|
| 描述符合路由表多個 entry（模糊命中） | 選擇 discipline 較高的路由（如 `/s4-tdd` 優於 `/s4-impl-task`），並以一行說明選擇原因。|
| 描述完全不符合任何路由 entry | 詢問：「這個任務是修 bug、加功能、環境設定，還是 debug？」|

---

## Step 1 — Mode Selection

掃描順序：

1. 先掃描 **mode signal**（見 Mode Signal Detection）。偵測到 `--vibe` 或 `--hotfix` → 進入對應模式，跳過 Greenfield Check。
2. **Greenfield Check**：`RULES.md` 存在 → Standard Mode；不存在 → Express Mode。

---

## Express Mode — 3-Question Interview

*適用：RULES.md 不存在的 greenfield 專案*

印出 HARD-GATE Express 確認文字後，逐一問以下三個問題，等待回答後再問下一題：

- **Q1**: *「語言和框架？（例：Python + FastAPI）」*
- **Q2**: *「有沒有絕對不能動的約束？（沒有則輸入「無」）」*
- **Q3**: *「任務完成後什麼會存在或停止壞掉？一句話。」*

三題全答後，**立刻寫入以下 artifacts**（不等用戶確認）：

- **RULES.md**（根目錄）：tech stack（Q1）+ constraints（Q2；若「無」寫 "none declared"）+ coverage 預設 80%
- **CONTEXT.md**（根目錄）：domain glossary（從 Q3 萃取 1–3 個核心名詞 + 說明）+ active task（Q3）
- **TASK_DAG.md**（根目錄，若已存在則跳過）：單節點 checklist，title = Q3 答案

寫入完成後，以 Q3 作為任務描述直接進入 Routing Table。

---

## Standard Mode — The One Question

*適用：RULES.md 已存在的 brownfield 專案*

印出 HARD-GATE Standard 確認文字後，問一個問題：

> *"What's the task? Describe it in one sentence — what breaks or what should exist after you're done."*

Wait for the answer. Then route immediately.

---

## Mode Signal Detection

**Before routing**, scan the task description for mode signals. Mode signal **overrides** task-type routing — `"fix null pointer --vibe"` activates Vibe Mode, not the bug-fix TDD route.

| If the description contains… | Mode | Action |
|---|---|---|
| `--vibe`, "prototype", "throwaway", "just exploring", "spike", "try out" | **Vibe Mode** | Print Vibe confirmation (below). Wait for Y. |
| `--hotfix`, "quick fix", "legacy codebase", "no tests here" | **Hotfix Mode** | Print Hotfix announcement (below). Use task-type routing. |
| None of the above | **Standard** | Use the Routing Table below normally. |

### Vibe Mode — Required Confirmation

Print this verbatim and wait for Y before routing:

```
⚡ Vibe Mode activated.
   - Routing directly to /s4-impl-task — TDD is optional.
   - s5 review is skipped for this session.
   - You MUST tag every commit [WIP/Prototype]. This creates tech debt.
   Confirm? (Y/n)
```

If the user says N, fall back to Standard Mode.

After Y: route to `/s4-impl-task`. Do NOT go through `/s4-tdd`.

### Hotfix Mode — Announcement

Print this and then use the Routing Table normally:

```
🔧 Hotfix Mode: TDD preserved. Routing to /s4-tdd.
   Downstream s5 review will apply CRITICAL-only criteria.
```

---

## Routing Table

Based on the user's one-sentence description, pick the first matching route:

| Task type | Route to |
|-----------|----------|
| Bug fix — something is broken | `/s4-tdd` (write a failing test that reproduces the bug first) |
| New behavior in existing code | `/s4-tdd` (write failing test for the new behavior) |
| Exploratory / throwaway | *(caught by Mode Signal Detection above — confirm Vibe Mode first)* |
| Environment / tooling setup | `/s4-setup-env` |
| Debug an existing failure | `/s4-local-debug` |

If the description is ambiguous between two routes, pick the one that requires MORE discipline (e.g., prefer `/s4-tdd` over `/s4-impl-task`). State your routing choice and the reason in one line.

---

## What Is NOT Skipped

Fast-track skips ceremony, not discipline. The following apply regardless:

- **s4-tdd HARD-GATE**: No production code without a failing test first. No exceptions in Standard and Hotfix Modes.
  *Vibe Mode exception: user has explicitly confirmed tech debt — routing goes directly to `/s4-impl-task` without tests.*
- **s4-impl-task HARD-GATE**: All acceptance criteria must be stated before writing code.
- **BROWNFIELD MODE**: If the project has `mode: brownfield` in `RULES.md`, the brownfield coverage gate in s4-tdd applies automatically — you do not need to re-set it.
  若 `RULES.md` 不存在 → 假定 standard mode，不阻斷路由。

---

## What Is Skipped

| Skipped artifact | Express Mode | Vibe Mode | Why |
|-----------------|:---:|:---:|-----|
| `CONTEXT.md` glossary (s1) | ✅ 自動產生 | ⛔ 跳過 | Express: 從任務描述萃取；Vibe: 原型不需要 |
| `RULES.md` (s1) | ✅ 自動產生 | ⛔ 跳過 | Express: 3 問題最小化版本；Vibe: 接受 s5-7 不可用 |
| `TASK_DAG.md` (s3) | ✅ 自動產生 | ⛔ 跳過 | Express: 單節點；Vibe: 原型不需要 |
| PRD / Vision doc (s2) | ⛔ 跳過 | ⛔ 跳過 | 單任務範圍；一句話描述足夠 |
| WBS（s3） | ⛔ 跳過 | ⛔ 跳過 | 單 atomic task，不需要分解 |
| Architecture Design Doc (s3) | ⛔ 跳過 | ⛔ 跳過 | 無新子系統；變更是局部的 |

If during execution you discover the task is NOT atomic (it requires new subsystems, cross-module changes, or alignment with other teams), **stop and say so**:

> *"This task turned out to be larger than atomic scope. Fast-track is not the right fit.
>  Consider running /s2-capture-vision to properly scope it first."*

Do not silently expand scope. Surface it and let the user decide.

---

## Completion Report

Report status using exactly one of:
- **ROUTED_EXPRESS** — RULES.md not found; ran 3-Question Interview; generated RULES.md + CONTEXT.md + TASK_DAG.md; routed to s4. Full s5-7 pipeline is now available.
- **ROUTED** — RULES.md found (brownfield); printed skip confirmation; user is now in s4.
- **ROUTED_VIBE** — `--vibe` signal detected; user confirmed; routed to `/s4-impl-task` without TDD. s5-7 unavailable for this session.
- **ROUTED_HOTFIX** — `--hotfix` signal detected; routed to `/s4-tdd` with CRITICAL-only s5 criteria.
- **BLOCKED** — task scope turned out non-atomic (cross-module or new subsystem); stopped and warned user; suggested `/s2-capture-vision`.
- **NEEDS_CLARIFICATION** — task description was empty, too vague, or matched zero routing table entries; re-prompted user for a one-sentence description.

</what-to-do>

<supporting-info>

## When Fast-Track Is the Wrong Choice

Do not use this skill if any of the following are true:
- The user is starting a brand-new project with no existing codebase
- The task requires coordinating with other agents or teams
- The user is unsure what they want to build (use `/s0-brainstorm` instead)
- The task will touch more than 3 files across different modules
- Compliance, security, or architectural decisions are in scope

## Role Identity: Fast-Track Router
- **Mindset**: Remove friction, not discipline. The goal is to get to s4 faster — not to skip s4's rigor.
- **Upstream Dependency**: None. This is an entry point.
- **Downstream Target**: One of s4-tdd, s4-impl-task, s4-setup-env, or s4-local-debug.

## Process Flow

```
/s-fast-track
  → Mode Signal Detection
      --vibe   → Vibe confirmation (wait Y) → s4-impl-task
      --hotfix → Hotfix announcement       → s4-tdd
      standard → Greenfield Check
                   RULES.md missing → Express Mode (3Q interview → write artifacts) → Routing Table
                   RULES.md exists  → Standard Mode (1 question)                   → Routing Table
```

## Eval Fixtures

Fixtures 位於 `tests/fixtures/fast-track-cases.json`。

每個 fixture 包含：`description`（任務描述）、`expected_mode`（Standard / Vibe / Hotfix）、`expected_route`（目標 skill）。

冒煙測試：逐一對照 fixture 的 `expected_route` 與 skill 實際路由結果是否一致。

## Artifact Dependencies
- **Reads**: RULES.md（existence check — determines Express vs Standard mode）
- **Writes**: RULES.md, CONTEXT.md, TASK_DAG.md（Express Mode only; skipped if RULES.md already exists）

</supporting-info>
