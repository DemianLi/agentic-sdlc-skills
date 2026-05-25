---
name: s0-trace-feature
description: >
  Use when understanding existing feature implementation. Outputs Mermaid sequence
  diagram tracing call chains with boundaries/gaps. NOT for new features or design.
---

<HARD-GATE>
⛔ OUTPUT DISCIPLINE:
After presenting the artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed to /s3-eval-system."
Do NOT invoke /s3-eval-system or any other skill automatically.
</HARD-GATE>

<what-to-do>

**Code Archaeologist role**: Surface how features work as-is. Record confirmations, mark gaps.

### 絕對不要觸發的情境
| 情境 | 正確技能 |
|------|----------|
| 用戶想*評估功能變更的技術風險或爆炸半徑* | `/s3-eval-system` |
| 用戶想*新建一個功能*（未曾存在於 codebase） | `/s2-capture-vision` 或 `/s3-design-arch` |
| 用戶想*debug 某個功能失效* | `/s4-local-debug` |

**Notation**: `A → B` confirmed call; `[INFERRED: reason]` not found; `[external: name]` outside workspace; `[?]` referenced but not located. Never omit gaps.

### Step 0 — Input Validation

| 失敗情境 | 行為 |
|---------|------|
| 名稱過於模糊（如 "那個登入的東西"） | Re-prompt：「請提供 function 名稱、檔案路徑，或描述 UI 入口點。」|
| 搜尋所有定義模式後找不到任何 entry point | BLOCKED — 回報：「在 codebase 中找不到 `<name>` 的 entry point，請確認名稱或提供檔案路徑。」|
| 用戶描述符合多個不同 feature | 列出候選清單，請用戶選擇一個後繼續。|

### Step 1 — Feature Scoping
Ask: **"Which feature do you want to trace?"** Accept: feature name, user action, route, or file path.

### Step 2 — Entry Point Discovery
Scan: frontend handlers/routes, backend routes/handlers, CLI commands, event consumers. Present candidates and **wait for user confirmation**.

### Step 3 — Full Chain Trace
Trace workspace (frontend → API → backend → DB). Read implementation, do not assume. Mark boundaries `[external: ...]`, missing links `[?]`. Note side effects, DB tables, data flows at boundaries.

### Step 4 — Confidence Check
**C1**: Entry point `[INFERRED]`? **C2**: Broken link `A → [?] → B`? **C3**: Core logic `[INFERRED]`?
If any true: prepend `⚠️ LOW CONFIDENCE` block, ask "Proceed or investigate further?"

### Step 5 — Write Output
Write to `docs/traces/YYYY-MM-DD-<feature-slug>.md` with Mermaid diagram, business logic, confirmed facts, gaps, boundary map. Commit to git. If commit fails → DONE_WITH_CONCERNS.

## Red Flags
| Flag | Action |
|---|---|
| Behavior described without reading source | You are guessing—open the file. |
| Skipped hop between confirmed nodes | Mark as `[?]`—every hop must be sourced. |
| Cannot explain data crossing a boundary | Read the caller's implementation. |

## Completion Report

- **DONE** — trace complete, all nodes confirmed, file committed.
- **DONE_WITH_CONCERNS** — with `⚠️ LOW CONFIDENCE` block; list C1/C2/C3 conditions.
- **BLOCKED** — entry point not found; state what was searched.
- **NEEDS_CONTEXT** — missing workspace access; state what is inaccessible.

</what-to-do>

<supporting-info>

## Artifact Standard
- **Output path**: `docs/traces/YYYY-MM-DD-<feature-slug>.md`
- **Required sections**: Sequence Diagram / Business Logic Summary / Confirmed Facts / Gaps & Unknowns / Boundary Map
- **Commit to git before reporting DONE**

Output voice: Name files, functions, line numbers. Be concrete, not general.

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-trace-feature/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: codebase source files (read-only scan)
- **Writes**: `docs/traces/YYYY-MM-DD-<feature>-trace.md`

</supporting-info>