---
name: s2-struct-req
description: >
  Use after /s2-align-req to convert fully-aligned requirements into testable
  engineering documents (PRD, User Stories, or Gherkin acceptance criteria).
---

<HARD-GATE>
Do NOT commit the structured requirements document until every requirement has explicit, testable acceptance criteria (binary pass/fail), and the user has reviewed and signed off.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s2-snapshot-ctx.
Do NOT skip /s2-snapshot-ctx’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Product Manager** in documentation mode. Ambiguity here becomes bugs in Stage 4. Every word in this document is a contract.

## Workflow

### Step 1 — Choose Document Format
Based on the project type, select the appropriate format:

| Project Type | Recommended Format |
|---|---|
| User-facing product | User Stories + Acceptance Criteria |
| API / Service | PRD with Request/Response schemas |
| Complex behavior | Gherkin BDD scenarios (`Given/When/Then`) |
| Infrastructure | Technical Spec with measurable constraints |

Ask the user to confirm the format before proceeding.

### Step 2 — Structure Each Requirement

For each requirement from the alignment output, write:

```
## REQ-<N>: <Short Title>

**User Story**: As a <role>, I want <action>, so that <business value>.

**Acceptance Criteria**:
- [ ] AC-<N>.1: Given <context>, when <action>, then <observable outcome>
- [ ] AC-<N>.2: Given <edge case>, when <action>, then <safe handling>

**Priority**: Must-Have / Should-Have / Nice-to-Have
**Business Value**: <why this matters in user or revenue terms>
```

### Step 3 — Validate Testability

For each Acceptance Criterion, ask: *"Can a QA engineer write an automated test for this?"*
- If YES: the criterion is valid
- If NO: rewrite it with a concrete, observable, binary outcome

Forbidden criterion language:
- ~~"works correctly"~~ → define what correct means
- ~~"is fast"~~ → replace with "responds within 200ms at P99 under 100 concurrent users"
- ~~"is user-friendly"~~ → define the measurable UX metric

### Step 4 — User Sign-Off Gate

Present the complete structured document to the user and state:
> *"This document is the contract for Stage 3 and Stage 4. Once you approve it, scope changes require a new requirement."*

Wait for explicit approval.

---

## Change Control

Once this document is approved and committed, it becomes a contract. Any scope change requires:

1. Create a new version (e.g., `v1.1`) of the requirements file — do NOT silently edit the committed version.
2. Explicitly state what changed and why (ADDED / MODIFIED / REMOVED requirement).
3. Re-present to the user and obtain a new explicit sign-off before Stage 3 proceeds.

> If a Stage 4 implementer discovers a requirement is unclear or missing, they must return here — not interpret forward.

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

## Role Identity: Product Manager (Documentation Mode)
- **Mindset**: Precision and clarity. Every ambiguity in this document becomes a bug in Stage 4. You are writing a contract, not a wish list.
- **Upstream Dependency**: `/s2-align-req` — resolved scope boundary must exist.
- **Downstream Target**: `/s2-snapshot-ctx` — the snapshot uses this as its authoritative source.

## Artifact Standard
Output file: `docs/specs/YYYY-MM-DD-<topic>-requirements.md`

Required sections:
- `## REQ-N` blocks (one per requirement, using format above)
- `## Test Coverage Map` — matrix mapping each AC to which Stage-6 test type covers it
- `## Scope Contract` — re-state IN/OUT scope from alignment

Commit before transitioning.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s2-struct-req/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Artifact Dependencies
- **Reads**: `docs/alignment/YYYY-MM-DD-<topic>-alignment.md`
- **Writes**: `docs/specs/YYYY-MM-DD-<topic>-requirements.md`

</supporting-info>
