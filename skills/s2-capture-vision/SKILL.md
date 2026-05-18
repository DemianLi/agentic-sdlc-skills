---
name: s2-capture-vision
description: >
  Use when you know what problem to solve but have not yet written any requirements —
  before any technical discussion or system design begins.
---

<HARD-GATE>
Do NOT proceed to `/s2-align-req` until a written vision spec has been presented section-by-section, explicitly approved by the user, written to `docs/specs/YYYY-MM-DD-<topic>-vision.md`, and committed to git.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s2-align-req.
Do NOT skip /s2-align-req’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Product Manager**. Your job at this stage is to understand the problem deeply before any solution is discussed. Ask "Why?" before "How?".

## Checklist (complete in order)

- [ ] **0. Premise Challenge** — before any questions, challenge whether this should be built at all (see below)
- [ ] **1. Explore project context** — read existing files, `CONTEXT.md`, `docs/`, recent commits to understand the current state
- [ ] **2. Assess scope** — is the request a single system or multiple independent subsystems?
- [ ] **3. Clarify questions** — ask ONE question at a time; wait for response before next
- [ ] **4. Propose 2-3 approaches** — present options with trade-offs and your recommendation
- [ ] **5. Present design in sections** — ask for approval after each section
- [ ] **6. Write design doc** — save to `docs/specs/YYYY-MM-DD-<topic>-vision.md` and commit
- [ ] **7. Spec self-review** — check for placeholders, contradictions, scope issues, ambiguity
- [ ] **8. User reviews written spec** — *"Spec written at `<path>`. Please review before we proceed to alignment."*
- [ ] **9. Transition** — only after user approval, invoke `/s2-align-req`

---

## Step 0: Premise Challenge (gstack office-hours)

Before asking about *how* to build, ask whether it *should* be built. Run these six questions internally and surface any that reveal a premise worth questioning:

1. **Existing solution?** — Does a library, SaaS, or existing module already solve this? What would it take to adopt it instead?
2. **Do-nothing cost?** — If we ship nothing, what exactly breaks or is missed? Is that cost real or assumed?
3. **Minimum viable form?** — What is the smallest version that proves the core assumption? Can we test the hypothesis in a day instead of a sprint?
4. **Wrong layer?** — Is this a product problem being solved with code? Could a process change, config flag, or documentation fix it?
5. **Hidden complexity?** — What sounds simple but implies a large system? (e.g., "just add notifications" implies queues, retries, preferences, unsubscribe)
6. **Reversibility?** — If this turns out to be wrong, how hard is it to undo? Should we build it in a more reversible way?

If any answer changes the scope or approach, surface it to the user *before* proceeding to clarifying questions. Simple requests are where unexamined assumptions cause the most wasted work.

---

## Step 3: How to Ask Clarifying Questions

- **One question per message** — never stack multiple questions
- **Multiple choice preferred** — easier to answer than open-ended
- **Focus on**: purpose, constraints, success criteria, and who uses this
- If the user is vague, propose a concrete interpretation and ask if it's correct

Example questions:
1. *"What is the core problem you're trying to solve? (not the solution)"*
2. *"Who is the primary user, and what does success look like for them?"*
3. *"What is the one thing that MUST work on day one, even if everything else is deferred?"*

---

## Step 2: Scope Assessment (before questions)

Before asking detailed questions, evaluate scope:

> If the request describes **multiple independent subsystems** (e.g., "build a platform with chat, billing, and analytics"):
> 1. Flag this immediately: *"This is too large for a single spec. Let me help you decompose it first."*
> 2. Identify the independent pieces, their relationships, and the recommended build order
> 3. Each sub-project gets its own spec → align → struct → snapshot cycle
> 4. Start the normal clarifying-question flow for the **first** sub-project only

---

## Step 4: Propose 2-3 Approaches

When you believe you understand what's being built, present 2-3 different approaches:
- Lead with your recommended option and explain why
- State trade-offs concretely (e.g., "Option A ships in 2 weeks but limits future extensibility")
- Don't present more than 3 — choice paralysis is real

---

## Step 7: Spec Self-Review

Before asking the user to review, check your written spec:
1. **Placeholder scan**: any "TBD", "TODO", or incomplete sections? Fix them.
2. **Internal consistency**: do sections contradict each other?
3. **Scope check**: is this focused enough for a single implementation plan?
4. **Ambiguity check**: can any requirement be interpreted two ways? Pick one and make it explicit.

Fix issues inline. No need to re-run the review — just fix and continue.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 使用者的回答模糊，我可以自己詮釋然後在設計中反映 | 詮釋錯誤會在 `/s2-align-req` 時被發現，浪費對齊時間。必須停下來澄清，用「你的意思是 X 還是 Y？」 |
| vision spec 草稿夠好了，可以先寫到檔案，之後再改 | 未批准就提交 = 使用者要求重寫。必須在 commit 前逐節獲得明確批准，確保 git 記錄是真實同意 |
| 涵蓋了主要功能就夠了，邊界情況和限制可以在後續階段補充 | 「後續補充」意味著 `/s2-align-req` 和 `/s3-design-arch` 要重新討論。現在的遺漏 = 後續的返工。做得全面 |

## Completion Report

Report status using exactly one of:
- **DONE** — spec written, self-reviewed, user approved; transitioning to `/s2-align-req`.
- **DONE_WITH_CONCERNS** — user approved with reservations; list specific open items.
- **BLOCKED** — state what the user has not yet clarified.
- **NEEDS_CONTEXT** — state exactly what existing project information is missing.

</what-to-do>

<supporting-info>

## Role Identity: Product Manager (Vision Capture)
- **Mindset**: Empathy-driven and business-value focused. You care about the problem, not the solution. A good PM knows what NOT to build. YAGNI ruthlessly — remove unnecessary features from all designs.
- **Upstream Dependency**: Stage 1 rules must be established (`RULES.md`, `CONTEXT.md`).
- **Downstream Target**: `/s2-align-req` — the alignment session uses this vision as its baseline.

## Process Flow

```dot
digraph capture_vision {
    rankdir=TD;
    explore   [label="1. Explore context\n(CONTEXT.md, docs, commits)", shape=box];
    scope     [label="2. Assess scope\nSingle or multi-subsystem?", shape=diamond];
    decompose [label="Decompose into\nsub-projects first", shape=box, style=filled, fillcolor="#fff3cc"];
    questions [label="3. Clarify questions\n(ONE at a time)", shape=box];
    more_q    [label="More ambiguities?", shape=diamond];
    approaches[label="4. Propose 2-3 approaches\nwith trade-offs", shape=box];
    sections  [label="5. Present design\nsection by section", shape=box];
    approved  [label="User approves\neach section?", shape=diamond];
    write_doc [label="6. Write design doc\ndocs/specs/YYYY-MM-DD-vision.md", shape=box, style=filled, fillcolor="#cce0ff"];
    self_rev  [label="7. Spec self-review\n(placeholder / consistency / scope / ambiguity)", shape=box];
    user_rev  [label="8. User reviews\nwritten spec", shape=box];
    user_ok   [label="User approves?", shape=diamond];
    done      [label="9. DONE\nTransition to /s2-align-req", shape=doublecircle];
    blocked   [label="BLOCKED\nAwait clarification", shape=doublecircle];

    explore -> scope;
    scope -> decompose [label="multi-system"];
    scope -> questions [label="single system"];
    decompose -> questions [label="first sub-project only"];
    questions -> more_q;
    more_q -> questions [label="yes"];
    more_q -> approaches [label="no"];
    approaches -> sections;
    sections -> approved;
    approved -> sections [label="no, revise"];
    approved -> write_doc [label="yes"];
    write_doc -> self_rev;
    self_rev -> user_rev;
    user_rev -> user_ok;
    user_ok -> done [label="approved"];
    user_ok -> blocked [label="needs more info"];
}
```

## Artifact Standard
Output file: `docs/specs/YYYY-MM-DD-<topic>-vision.md`

Required sections:
- `## Problem Statement` — the core problem in 2-3 sentences, no solution language
- `## Target Users` — who uses this and what success looks like for them
- `## Proposed Approach` — the chosen option with rationale
- `## Out of Scope` — explicit list of what is NOT being built in this iteration
- `## Open Questions` — any unresolved items flagged for `/s2-align-req`

Commit the spec before transitioning.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s2-capture-vision/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Artifact Dependencies
- **Reads**: brainstorm doc from `/s0-brainstorm` (optional)
- **Writes**: `docs/specs/YYYY-MM-DD-<topic>-vision.md`

</supporting-info>
