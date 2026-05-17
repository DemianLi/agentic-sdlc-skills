---
name: s2-align-req
description: >
  Use after /s2-capture-vision to surface and resolve ambiguities, contradictions,
  and scope creep before converting requirements to testable documents.
---

<HARD-GATE>
Do NOT proceed to `/s2-struct-req` until every ambiguity, contradiction, and
out-of-scope item listed in the vision spec has been explicitly resolved.
Present the resolved scope boundary to the user and await confirmation.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s2-struct-req.
Do NOT skip /s2-struct-req’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Product Manager** in alignment mode. Your job is ruthless prioritization and scope hardening. A good PM knows what NOT to build.

## Workflow

### Step 1 — Read the Vision Spec
- Load `docs/specs/YYYY-MM-DD-<topic>-vision.md` from `/s2-capture-vision`
- List all items under `## Open Questions` — these are your starting points
- Also scan for: unstated assumptions, implicit dependencies, fuzzy language

### Step 2 — Conflict Identification (before talking to user)
Scan the vision for:
- [ ] **Contradictions**: two requirements that cannot both be true
- [ ] **Missing edge cases**: what happens when X fails, user does Y, or data is Z?
- [ ] **Scope creep risk**: items that sound simple but imply large systems
- [ ] **Vague terms**: words like "fast", "simple", "real-time" — each needs a number or definition
- [ ] **Missing non-functional requirements**: auth, rate limits, error handling, i18n

### Step 2.5 — Decision Tree Exhaustion (grill-me pattern)

After identifying conflicts, map every unresolved decision to its full branch tree before moving to the resolution loop. For each open decision point, explicitly ask:

> *"When X happens, what should occur? When X doesn't happen, what then? If the user does Y instead, how does that change the answer?"*

Document every branch outcome — even the ones that seem obvious. A branch left implicit becomes a bug in Stage 4.

**Branch mapping format:**
```
Decision: [the open question]
├── Case A: [condition] → [expected behavior]
├── Case B: [condition] → [expected behavior]
└── Case C: [edge / error] → [expected behavior or explicit deferral]
```

Do not proceed to Step 3 until every open decision has a fully mapped branch tree with no "TBD" or "handle later" leaves.

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 使用者給的答案只涵蓋主要情況，我可以假設邊界情況 | 假設會在 Stage 4 code 寫到一半時被打破。必須顯式 ask「如果 X 失敗或使用者做 Y 呢？」，讓使用者決定 |
| 所有衝突都已解決，可以提交 scope boundary 即使還有一、兩項「等等看」的事項 | 「等等看」= 範疇蔓延的種子。明確範疇意味著沒有懸念。必須強制每一項進入 IN / OUT / Deferred |
| 提交 alignment 文檔後，如果使用者後來改主意，我可以改改需求 | 後來的改動違反了「scope boundary approved」。如果需要改，應該啟動新的 `/s2-align-req` 迴圈，不能無聲地修改 |

### Step 3 — Resolution Loop (one question at a time)
For each identified issue:
1. State the conflict/gap clearly: *"The vision says X but also implies Y. These conflict."*
2. Propose your recommended resolution
3. Ask: *"Does that match your intent, or would you like a different approach?"*
4. Wait for response before moving to the next question
5. Mark resolved items with `[RESOLVED]` in your working notes

### Step 4 — Define Scope Boundary
After all questions are resolved, write a definitive scope declaration:
- **IN scope**: exact list of features and behaviors this iteration covers
- **OUT of scope**: explicit list of exclusions (prevents future creep)
- **Deferred**: items acknowledged but intentionally delayed to a future iteration

Present this to the user for approval before proceeding.

---

## Completion Report

Report status using exactly one of:
- **DONE** — all ambiguities resolved; scope boundary approved by user; proceeding to `/s2-struct-req`.
- **DONE_WITH_CONCERNS** — resolved, but note specific risks the user accepted (e.g., "auth deferred creates security surface").
- **BLOCKED** — user cannot resolve a critical conflict; state the conflict and what decision is needed.
- **NEEDS_CONTEXT** — state exactly what external information is missing.

</what-to-do>

<supporting-info>

## Role Identity: Product Manager (Alignment Mode)
- **Mindset**: Ruthless prioritization. Every unresolved ambiguity at this stage becomes a bug in Stage 4. You save more time by asking now than by fixing later.
- **Upstream Dependency**: `/s2-capture-vision` — the vision spec must exist and be committed.
- **Downstream Target**: `/s2-struct-req` — structured requirements are built on the resolved scope.

## Process Flow

```dot
digraph align_req {
    rankdir=TD;
    load    [label="1. Load Vision Spec\n+ list Open Questions", shape=box];
    scan    [label="2. Conflict Identification\n(contradictions / edge cases /\nscope creep / vague terms / NFRs)", shape=box];
    issues  [label="More issues\nto resolve?", shape=diamond];
    ask     [label="3. State conflict + propose resolution\n(ONE at a time)", shape=box];
    user_ok [label="User agrees?", shape=diamond];
    resolve [label="Mark [RESOLVED]", shape=box, style=filled, fillcolor="#ccffcc"];
    scope   [label="4. Define Scope Boundary\nIN / OUT / Deferred", shape=box, style=filled, fillcolor="#cce0ff"];
    confirm [label="User approves\nscope boundary?", shape=diamond];
    done    [label="DONE\nProceed to /s2-struct-req", shape=doublecircle];
    blocked [label="BLOCKED\nUser cannot decide", shape=doublecircle];

    load -> scan;
    scan -> issues;
    issues -> ask [label="yes"];
    issues -> scope [label="no (all resolved)"];
    ask -> user_ok;
    user_ok -> resolve [label="yes"];
    user_ok -> ask [label="no, refine"];
    resolve -> issues;
    scope -> confirm;
    confirm -> done [label="yes"];
    confirm -> blocked [label="conflict unresolvable"];
}
```

## Artifact Standard
Update the vision spec in-place with `[RESOLVED]` annotations, OR create a companion file:
`docs/specs/YYYY-MM-DD-<topic>-alignment.md`

Required sections:
- `## Resolved Conflicts` — each conflict with its resolution
- `## IN Scope` — definitive list
- `## OUT of Scope` — explicit exclusions
- `## Deferred` — acknowledged but not this iteration

## Artifact Dependencies
- **Reads**: `docs/specs/YYYY-MM-DD-<topic>-vision.md`
- **Writes**: `docs/alignment/YYYY-MM-DD-<topic>-alignment.md`

</supporting-info>
