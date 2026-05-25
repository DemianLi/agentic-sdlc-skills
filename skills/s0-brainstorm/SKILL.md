---
name: s0-brainstorm
description: >
  Use when clarifying a vague problem before speccing. Outputs problem statement
  draft (not spec, not design). NOT for well-defined feature requirements.
---

<HARD-GATE>
⛔ OUTPUT DISCIPLINE:
After presenting the artifact, your message MUST end with exactly:
  "Awaiting your approval. If you'd like to develop this further, run /s2-capture-vision with this draft as input."
Do NOT invoke /s2-capture-vision or any other skill automatically.
</HARD-GATE>

<what-to-do>

**Problem Scout role**: Help user understand their actual problem — not propose solutions. Diverge before converge; every idea valid until reality-checked.

### 絕對不要觸發的情境

| 情境 | 改用 |
|------|------|
| 你已有明確的功能需求（e.g., "我要做一個 user login 功能"） | `/s2-capture-vision` — 問題已清楚，直接進 vision capture |
| 你在調查一個已知 bug 或錯誤 | `/s4-local-debug` — 診斷流程，不是問題探索 |
| 你想驗證現有 spec 是否完整 | `/s0-trace-feature` — spec 驗證，非問題發現 |

### Step 0 — Input Validation

此 skill 的輸入是用戶的口頭或文字描述，無需預存文件。

| 失敗情境 | 行為 |
|---------|------|
| 用戶對問題完全沒有描述（只說「不知道」）| Re-prompt：「請描述一個讓你感到困擾或想改變的事情，哪怕只是一個感覺。」|
| 用戶已提供清楚功能需求（非模糊感覺）| 停止並提示：「你的需求已足夠清楚，建議使用 `/s2-capture-vision` 直接進入需求捕捉。」|

### Step 1 — Empty the Container
User describes vague feeling/frustration without structure. Reflect back: "What I'm hearing is: [paraphrase]. Is that roughly right?" One reflection, then wait.

### Step 2 — Visual Questions
Ask 2–3 of these, one at a time: pain moment, day-in-life if solved, current workaround, who has it, what breaks.

### Step 3 — Map Problem Space
Fill table: Who (who suffers), Frequency, Cost, Workaround, Broken thing. Record unknowns as-is; do not invent.

### Step 4 — Generate Three Framings
Write three problem sentences starting "The real problem is…" from Lens A (user pain), Lens B (system), Lens C (missing abstraction). Do not hint preference.

### Step 5 — Reality-Check
For each: symptom or cause? already solved? worth solving? Mark each `REAL PROBLEM` / `SYMPTOM — dig deeper` / `ALREADY SOLVED`.

### Step 6 — User Chooses Framing
Ask: "Which feels closest to what you're solving?" Wait for explicit selection.

### Step 7 — Write Problem Draft
Write `docs/brainstorm/YYYY-MM-DD-<topic>-problem-draft.md`: chosen framing, problem space map, rejected framings, open questions, what this IS NOT. Create dir if needed.

## Completion Report

- **DONE** — problem statement draft written and committed; user chose a framing; ready for `/s2-capture-vision` if user decides to proceed.
- **DONE_WITH_CONCERNS** — draft written, but note if the chosen framing is still fuzzy or the reality-check revealed deep unknowns.
- **BLOCKED** — user cannot converge on any framing; state which framings were tried and why they were rejected.
- **NEEDS_CONTEXT** — the domain is too unfamiliar to generate meaningful framings; state what background is needed.

</what-to-do>

<supporting-info>

Output: `docs/brainstorm/YYYY-MM-DD-<topic>-problem-draft.md` (chosen framing, map, rejected framings, open questions, what NOT). Only output; no architecture, tech, hints.

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: none
- **Writes**: `docs/brainstorm/YYYY-MM-DD-<topic>-problem-draft.md` (optional — 產出可選)

</supporting-info>
