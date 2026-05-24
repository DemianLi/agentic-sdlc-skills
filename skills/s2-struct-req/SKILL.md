---
name: s2-struct-req
description: >
  Use when converting aligned requirements into testable engineering documents
  (PRD, User Stories, Gherkin). NOT for requirements lacking alignment.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)

1. Does any file matching `docs/specs/*-alignment.md` exist?
   - **No** → run `python skills/s0-eval-alignment/scripts/engine.py --suggest "docs/specs/*-alignment.md"`, report its output, and **STOP**.

Only proceed when an alignment doc is present.

---

Do NOT commit the structured requirements document until every requirement has explicit, testable acceptance criteria (binary pass/fail), and the user has reviewed and signed off.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s2-snapshot-ctx.
Do NOT skip /s2-snapshot-ctx’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Product Manager**. Every word is a contract; ambiguity becomes bugs in Stage 4.

## Workflow

### Step 1 — Choose Format
Select: **User Stories + Acceptance Criteria** | **PRD with schemas** | **Gherkin BDD** | **Technical Spec**. Ask user to confirm.

### Step 2 — Structure Each Requirement
For each requirement, write:
```
## REQ-<N>: <Title>
**User Story**: As a <role>, I want <action>, so that <value>.
**Acceptance Criteria**:
- [ ] AC-<N>.1: Given <context>, when <action>, then <outcome>
- [ ] AC-<N>.2: Given <edge case>, when <action>, then <handling>
**Priority**: Must-Have | Should-Have | Nice-to-Have
**Business Value**: <why this matters>
```

### Step 3 — Validate Testability
Ask: *"Can a QA engineer automate a test for this?"* Replace vague language:
- ~~"works correctly"~~ → "returns valid response within spec"
- ~~"is fast"~~ → "responds within 200ms at P99 under 100 concurrent users"
- ~~"user-friendly"~~ → "measurable UX metric"

### Step 4 — User Sign-Off
Present complete document: *"This is the contract for Stages 3–4. Approve to proceed."* Wait for explicit approval.

**Change Control**: After approval, versioning required for scope changes (v1.1). Stage 4 implementers must return here if requirements are unclear.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 某些需求很明顯怎麼測試，不需要寫明確的 AC 敍述 | 「明顯」在 Stage 4 變成 3 種詮釋。必須寫成 Gherkin 或具體敍述，讓 QA 和工程師都一致 |
| 文件還有一些 AC 是「性能良好」或「系統穩定」而不是數字 | 這些是不可測試的。必須改寫成「P99 latency < 200ms in load test with 100 concurrent users」。可測試 = 無歧義 |
| 使用者快速掃過要求就說「看起來不錯」，我可以直接 commit | 「看起來不錯」不是簽核。必須明確要求「你批准我提交嗎？」並等待「是的，提交」 |

## Completion Report

Report status using exactly one of:
- **DONE** — structured doc written, testability validated, user signed off. Proceeding to `/s2-snapshot-ctx`.
- **DONE_WITH_CONCERNS** — signed off but note requirements marked "Should-Have" or "Nice-to-Have" that may be cut.
- **BLOCKED** — user cannot define an acceptance criterion for a critical requirement.
- **NEEDS_CONTEXT** — state exactly what business context is missing.

</what-to-do>

<supporting-info>

## Artifact Standard
Output: `docs/specs/YYYY-MM-DD-<topic>-requirements.md`
Requires: `## REQ-N` blocks, `## Test Coverage Map` (AC to test type), `## Scope Contract` (IN/OUT scope). Commit before transitioning.

## Artifact Dependencies
- **Reads**: `docs/alignment/YYYY-MM-DD-<topic>-alignment.md`
- **Writes**: `docs/specs/YYYY-MM-DD-<topic>-requirements.md`

→ Full reference: `references/detail.md`

</supporting-info>
