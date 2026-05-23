---
name: s2-capture-vision
description: >
  Use when you know what problem to solve but have no requirements yet — outputs vision
  spec before any design begins. NOT for tasks with an existing PRD or spec.
---

<HARD-GATE>
Do NOT proceed to `/s2-align-req` until a written vision spec has been presented section-by-section, explicitly approved by the user, written to `docs/specs/YYYY-MM-DD-<topic>-vision.md`, and committed to git.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s2-align-req.
Do NOT skip /s2-align-req's own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

## Checklist (complete in order)

- [ ] **0. Premise Challenge** — challenge whether this should be built at all (see below)
- [ ] **1. Explore context** — read `CONTEXT.md`, `docs/`, recent commits
- [ ] **2. Assess scope** — single system or multiple independent subsystems?
- [ ] **3. Clarify questions** — ONE question at a time; wait for response before next
- [ ] **4. Propose 2-3 approaches** — options with trade-offs and your recommendation
- [ ] **5. Present design in sections** — get approval after each section
- [ ] **6. Write design doc** — save to `docs/specs/YYYY-MM-DD-<topic>-vision.md` and commit
- [ ] **7. Spec self-review** — check placeholders, contradictions, scope, ambiguity
- [ ] **8. User reviews written spec** — *"Spec written at `<path>`. Please review before we proceed."*
- [ ] **9. Transition** — only after user approval, invoke `/s2-align-req`

---

## Step 0: Premise Challenge

Run these six questions internally; surface any that reveal a premise worth questioning:

1. **Existing solution?** — Does a library, SaaS, or existing module already solve this?
2. **Do-nothing cost?** — If we ship nothing, what exactly breaks? Is that cost real or assumed?
3. **Minimum viable form?** — What is the smallest version that proves the core assumption?
4. **Wrong layer?** — Is this a product problem being solved with code?
5. **Hidden complexity?** — What sounds simple but implies a large system?
6. **Reversibility?** — If this turns out wrong, how hard is it to undo?

Surface any that change scope or approach *before* clarifying questions.

---

## Step 2: Scope Assessment

> If the request describes **multiple independent subsystems**:
> 1. Flag immediately: *"This is too large for a single spec. Let me decompose it first."*
> 2. Identify pieces, relationships, and recommended build order
> 3. Start clarifying questions for the **first** sub-project only

---

## Step 3: Clarifying Questions
- ONE per message; multiple choice preferred
- Focus: purpose, constraints, success criteria, primary user

## Step 4: Propose 2-3 Approaches
- Lead with recommendation + why; state trade-offs concretely; maximum 3 options

---

## Step 7: Spec Self-Review

1. **Placeholder scan**: any "TBD", "TODO", or incomplete sections? Fix them.
2. **Internal consistency**: do sections contradict each other?
3. **Scope check**: focused enough for a single implementation plan?
4. **Ambiguity check**: any requirement interpretable two ways? Pick one.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 用戶回答模糊，我可以自己詮釋 | 詮釋錯誤在 `/s2-align-req` 時被發現。停下來澄清。 |
| 草稿夠好了，先寫到檔案之後再改 | 未批准就提交 = 用戶要求重寫。逐節批准後再 commit。 |
| 涵蓋主要功能就夠了，邊界情況後補 | 「後補」= `/s2-align-req` 和 `/s3-design-arch` 要返工。 |

## Completion Report

- **DONE** — spec written, self-reviewed, user approved; transitioning to `/s2-align-req`.
- **DONE_WITH_CONCERNS** — user approved with reservations; list specific open items.
- **BLOCKED** — state what the user has not yet clarified.
- **NEEDS_CONTEXT** — state exactly what existing project information is missing.

</what-to-do>

<supporting-info>

## Artifact Dependencies
- **Reads**: brainstorm doc from `/s0-brainstorm` (optional)
- **Writes**: `docs/specs/YYYY-MM-DD-<topic>-vision.md` (sections: Problem Statement, Target Users, Proposed Approach, Out of Scope, Open Questions)

→ Full reference: `references/detail.md`

</supporting-info>
