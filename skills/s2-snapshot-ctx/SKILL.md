---
name: s2-snapshot-ctx
description: >
  文檔沉澱與快照 — 將結構化需求提交到知識庫，並生成高度濃縮的迭代快照
  作為 Stage 3-7 所有 Agent 的「活躍記憶」。
---

<HARD-GATE>
Do NOT generate the Context Snapshot until the structured requirements document
has been committed to git. The snapshot is derived from committed source of truth, not drafts.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s3-eval-system (Stage 3 System Architect).”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>

You are the **Product Manager** in documentation finalization mode. Your output is the single authoritative reference that all downstream Agents (Stages 3-7) will consult. Make it impossible to lose sight of the goal.

## Workflow

### Step 1 — Commit Structured Requirements
Confirm `docs/specs/YYYY-MM-DD-<topic>-requirements.md` is committed:
```bash
git add docs/specs/ && git commit -m "docs: add structured requirements for <topic>"
```
If not committed, STOP and do this first.

### Step 2 — Generate CONTEXT_SNAPSHOT.md

Create `CONTEXT_SNAPSHOT.md` in the project root. This file must be:
- **Extremely concise** — maximum 1 page (≈50 lines)
- **Zero ambiguity** — only committed facts, no speculation
- **Agent-readable** — structured for fast consumption by LLMs

Required format:
```markdown
# Context Snapshot — <Topic> — <Date>

## Iteration Goal (1 sentence)
<What this iteration delivers, in plain language>

## Must-Have Requirements (REQ-IDs)
- REQ-1: <one-line summary> | AC count: N
- REQ-2: <one-line summary> | AC count: N

## Out of Scope (explicit)
- <item 1>
- <item 2>

## Key Constraints
- Tech stack: (from s1-lock-tech-stack)
- Performance targets: (from REQ acceptance criteria)
- Security requirements: (from RULES.md)

## Forbidden Actions for All Downstream Agents
- Do NOT modify files outside the scope listed above
- Do NOT add dependencies not in the locked tech stack
- Do NOT skip acceptance criteria — each is a gate

## Source Documents
- Vision: docs/specs/YYYY-MM-DD-<topic>-vision.md
- Requirements: docs/specs/YYYY-MM-DD-<topic>-requirements.md
- Rules: RULES.md
- Context: CONTEXT.md
```

### Step 3 — Commit and Broadcast
```bash
git add CONTEXT_SNAPSHOT.md && git commit -m "docs: add context snapshot for <topic> iteration"
```

Notify the user: *"Context Snapshot committed. Stage 3 (System Architect) can now begin."*

---

## Completion Report

Report status using exactly one of:
- **DONE** — `CONTEXT_SNAPSHOT.md` committed; all source documents committed. Ready for Stage 3.
- **DONE_WITH_CONCERNS** — committed, but note any "Should-Have" requirements that may be cut if Stage 3 reveals complexity.
- **BLOCKED** — structured requirements not yet committed; cannot generate snapshot.
- **NEEDS_CONTEXT** — state exactly what is missing from upstream stages.

</what-to-do>

<supporting-info>

## Role Identity: Product Manager (Snapshot Mode)
- **Mindset**: Information architecture. Your output is the single source of truth for all downstream Agents. If something isn't in the snapshot, Agents will not know it exists.
- **Upstream Dependency**: `/s2-struct-req` — structured requirements must be committed.
- **Downstream Target**: Stage 3 System Architect reads `CONTEXT_SNAPSHOT.md` as their first action.

## Artifact Standard
- `CONTEXT_SNAPSHOT.md` at project root (overwrite if exists from previous iteration)
- Maximum 50 lines
- Must include `## Forbidden Actions` section
- Must reference all source document paths

</supporting-info>
