---
name: s-fast-track
description: >
  Use when routing atomic tasks (bug fixes, brownfield features) directly to s4.
  Outputs minimal RULES.md if needed. NOT for greenfield, cross-module, or spec.
---

<HARD-GATE>
⛔ MODE CONFIRMATION — do not proceed to s4 until the required interaction for the active mode is complete:

**Express Mode**（RULES.md 不存在）: print `"Express Mode: generating minimal artifacts (3 questions). Add --vibe to skip."` → 3-Question Interview → write artifacts → route.

**Standard Mode**（RULES.md 存在）: print `"Fast-track mode: RULES.md found — going directly to s4."` → ask ONE question → route.

**Vibe Mode**（`--vibe` flag）: print Vibe confirmation → wait for explicit Y → route. This is a second required gate.
</HARD-GATE>

<what-to-do>

**Fast-Track Router**: Skip ceremony, reach s4 fast. Keep engineering discipline intact.

## Step 0 — Input Validation
One-sentence task description required. Empty → re-prompt. Vague/3+ sentences → compress to one sentence. Multi-match → pick higher discipline route (e.g., s4-tdd over s4-impl-task). No match → ask: bug fix, new feature, setup, or debug?

---

## Step 1 — Mode Selection
Scan mode signals first. `--vibe` or `--hotfix` → corresponding mode. Otherwise: RULES.md exists → Standard; missing → Express.

## Express Mode — 3-Question Interview
Q1: Language/framework? Q2: Absolute constraints (or "none")? Q3: What exists/stops breaking after? Write RULES.md + CONTEXT.md + TASK_DAG.md automatically. Route to table with Q3.

## Standard Mode — The One Question
Print Standard confirmation. Ask: "Task in one sentence — what breaks or exists after?" Route immediately.

---

## Mode Signal Detection
**Before routing**, scan description for signals. Override task-type routing: `--vibe` / prototype / spike → Vibe. `--hotfix` / quick fix / legacy → Hotfix. None → Standard.

**Vibe Mode**: Print confirmation (TDD optional, s5 skipped, tag [WIP/Prototype]). Wait Y/n. If Y → `/s4-impl-task`.

**Hotfix Mode**: Print announcement (TDD preserved, s5 CRITICAL-only). Use Routing Table normally.

---

## Routing Table
Bug fix / new behavior → `/s4-tdd`. Environment / setup → `/s4-setup-env`. Debug failure → `/s4-local-debug`. Ambiguous → pick higher discipline (prefer s4-tdd). State reason one line.

**Not Skipped**: No production code without failing test first (Standard/Hotfix). All AC stated before code (s4-impl-task). Brownfield coverage gate applies if `RULES.md` exists.

**What Is Skipped**: PRD, WBS, Architecture doc (unnecessary for atomic scope). If task turns non-atomic (new subsystems, cross-module), stop and suggest `/s2-capture-vision`.

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

Routes to one of s4-tdd, s4-impl-task, s4-setup-env, s4-local-debug. Generates RULES.md + CONTEXT.md + TASK_DAG.md in Express Mode.

## Eval Fixtures

Fixtures located at `tests/fixtures/fast-track-cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: RULES.md（existence check — determines Express vs Standard mode）
- **Writes**: RULES.md, CONTEXT.md, TASK_DAG.md（Express Mode only; skipped if RULES.md already exists）

</supporting-info>
