---
name: s2-align-req
description: >
  Use when resolving vision ambiguities — decision trees, conflict surface. Outputs
  alignment doc. NOT for requirement writing.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s2-align-req`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

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

### Step 1 — Read the Vision Spec
- Load `docs/specs/YYYY-MM-DD-<topic>-vision.md` from `/s2-capture-vision`
- List all items under `## Open Questions` — these are your starting points
- Also scan for: unstated assumptions, implicit dependencies, fuzzy language

### Step 2 — Conflict Scan

Identify: contradictions, missing edge cases, scope creep, vague terms, missing NFRs.

Then **map every decision** to full branch tree:
```
Decision: [question]
├── Case A: [condition] → [behavior]
├── Case B: [condition] → [behavior]
└── Case C: [edge/error] → [behavior or deferral]
```

No "TBD" leaves. Every branch must have explicit outcome.

### Step 3 — Resolution Loop (One at a time)

For each conflict:
1. State the conflict clearly
2. Propose resolution
3. Ask: "Does that match your intent?"
4. Wait for response
5. Mark `[RESOLVED]`

### Step 4 — Define Scope Boundary

Write definitive scope:
- **IN scope**: exact features this iteration
- **OUT of scope**: explicit exclusions
- **Deferred**: acknowledged, future iteration

Present to user for final approval.

## Completion Report

Report status using exactly one of:
- **DONE** — all ambiguities resolved; scope boundary approved by user; proceeding to `/s2-struct-req`.
- **DONE_WITH_CONCERNS** — resolved, but note specific risks the user accepted (e.g., "auth deferred creates security surface").
- **BLOCKED** — user cannot resolve a critical conflict; state the conflict and what decision is needed.
- **NEEDS_CONTEXT** — state exactly what external information is missing.

</what-to-do>

<supporting-info>

**Reads**: `docs/specs/YYYY-MM-DD-<topic>-vision.md`  
**Writes**: `docs/alignment/YYYY-MM-DD-<topic>-alignment.md`

## Eval Fixtures

Fixtures located at `tests/fixtures/s2-align-req/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
