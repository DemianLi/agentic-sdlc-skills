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

**System Architect (design mode)**: Output is a contract. Every downstream implementer and auditor holds you to exactly what you write.

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

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: `docs/arch/YYYY-MM-DD-<topic>-impact.md`, RULES.md
- **Writes**: `docs/arch/YYYY-MM-DD-<topic>-design.md`

</supporting-info>
