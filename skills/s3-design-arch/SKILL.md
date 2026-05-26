---
name: s3-design-arch
description: >
  Use when designing system architecture after impact analysis. Outputs OpenSpec
  document with data structures, API contracts, sequence diagrams. NOT for scoping.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s3-design-arch`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed to `/s3-breakdown-wbs` until:
1. The OpenSpec design document has been written and COMMITTED to git.

A design that exists only in memory is not an artifact; it is an intention.
`/s3-breakdown-wbs` reads `docs/arch/YYYY-MM-DD-<topic>-design.md` — if that file
does not exist on disk and in git, the next stage has nothing to read and cannot start.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s3-breakdown-wbs.
Do NOT skip /s3-breakdown-wbs’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

**System Architect**: Output is a contract. Every downstream implementer and auditor holds you to exactly what you write.

## Mode Selection

If the user does not specify, ask: "Is this new design or refactoring existing code?"

| 模式 | 使用時機 | 輸入 |
|------|---------|------|
| `new-design` (default) | 新功能、新系統、空白設計 | impact report from `/s3-eval-system` |
| `refactor-existing` | 重構、改善現有架構 | 現有代碼路徑 + 相關 ADR 文件 |

---

## Mode A: new-design

## Design Document Format (OpenSpec)

Create `docs/arch/YYYY-MM-DD-<topic>-design.md` with:

### Section 1 — Context
State problem, constraints (from RULES.md), assumptions.

### Section 2 — Decision
State chosen approach, rationale, rejected alternatives.

### Section 3 — Data Structures
Typed schemas for every data model.

### Section 4 — API Contracts
For each endpoint: request, response (200), error responses.

### Section 5 — Sequence Diagrams
Mermaid diagram for happy path (minimum) + error flows.

### Section 6 — Consequences
Positive outcomes, negative trade-offs, identified risks.

### Section 7 — Delta Spec
Change ID, Added/Modified/Removed/Unchanged components with traceability.

1. Read impact report from `/s3-eval-system` and `RULES.md`
2. **Input Sanity Check**: Impact report lists specific files (not "the service layer"); breaking changes state exact contract changes; recommended approach exists. If any fail, **stop and state exactly what is missing.**
3. Write sections 1-7
4. Present **section by section** — ask approval after each before continuing
5. After all approved, commit and proceed to `/s3-breakdown-wbs`

---

## Mode B: refactor-existing

1. **Read existing code**: Read the files the user specifies (or infer from context). Identify: current architectural boundaries, coupling patterns, and which ADRs govern these files.
2. **Read ADRs**: Load relevant `docs/arch/*.md` — identify existing decisions and their rationale. Do NOT propose changes that violate a standing ADR without flagging the conflict first.
3. **Architectural Assessment**: Identify issues in the existing code:
   - Coupling violations (components that depend on implementation details)
   - Boundary erosion (logic that has drifted across layers)
   - ADR drift (code that contradicts a standing architectural decision)
   - Testability gaps (structures that make unit testing hard)
4. **Propose Changes** using the same OpenSpec format (Sections 1–7), with these adjustments:
   - Section 1 (Context): Describe the existing state and what problems it creates
   - Section 2 (Decision): State the refactor approach and what alternatives were rejected
   - Section 7 (Delta Spec): List what changes, what stays, and what gets removed — with specific file paths
5. Present **section by section** — ask approval after each before continuing
6. After all approved, commit and proceed to `/s3-breakdown-wbs`

**Input Sanity Check (refactor mode)**: User has specified target files or modules; at least one concrete architectural problem is named; relevant ADRs are readable. If any fail, **stop and state exactly what is missing.**

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "我已經在代碼中看到類似的模式，設計應該是一致的" | 設計文件必須獨立自 RULES.md 和影響報告；不能靠「我假設代碼已經對了」 |
| "用戶對粗略版本的序列圖點頭，細節可以 s4 再調整" | Mermaid 圖是 s3-breakdown-wbs 拆解任務的依據；細節變更必須重新呈現 |
| "OpenSpec 還沒完全寫完，但 API schema 核心部分已經 OK 了" | 「還沒完成」= 還沒提交；不能分部分批准 |

## Completion Report

- **DONE** — OpenSpec written, all sections approved, committed. Proceeding to `/s3-breakdown-wbs`.
- **DONE_WITH_CONCERNS** — approved with reservations; list open architectural questions.
- **BLOCKED** — design conflicts with an existing ADR or RULES.md constraint; state the conflict.
- **NEEDS_CONTEXT** — state exactly what technical information is missing.

</what-to-do>

<supporting-info>

Output: `docs/arch/YYYY-MM-DD-<topic>-design.md` with 7 required sections. Commit before transitioning.

## Eval Fixtures

Fixtures located at `tests/fixtures/s3-design-arch/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: `docs/arch/YYYY-MM-DD-<topic>-impact.md`, RULES.md
- **Writes**: `docs/arch/YYYY-MM-DD-<topic>-design.md`

</supporting-info>
