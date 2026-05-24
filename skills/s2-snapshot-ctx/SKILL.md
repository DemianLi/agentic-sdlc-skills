---
name: s2-snapshot-ctx
description: >
  Use when freezing committed requirements into a compact context snapshot for
  downstream agents. Outputs CONTEXT_SNAPSHOT.md. NOT before requirements commit.
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

You are the **Product Manager**. Your snapshot is the single authoritative reference for all downstream agents.

## Workflow

### Step 1 — Verify Requirements Committed
Confirm `docs/specs/YYYY-MM-DD-<topic>-requirements.md` exists in git. If not, **STOP** — do not proceed until committed.

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 我可以從記憶或未提交的草稿生成 snapshot，事後再 commit 需求文檔 | 不行。snapshot 必須來自 committed 的事實。未 commit = 草稿，可能被使用者改掉。必須先 commit，再衍生 |
| snapshot 可以包含我的詮釋或預測，幫助下一階段的 Agent | 不行。只能轉錄 committed 事實。詮釋和預測會在 Stage 3 被推翻。保持純粹 |
| 如果 snapshot 超過 1 頁，可以放心加入更多背景資訊 | 不行。1 頁限制是刻意的。Stage 3-7 Agent 需要快速掃描。冗長 = 被忽視。刪除非關鍵項 |

### Step 2 — Generate CONTEXT_SNAPSHOT.md
Create `CONTEXT_SNAPSHOT.md` in project root, ≤50 lines. Format:
```
# Context Snapshot — <Topic> — <Date>
## Iteration Goal (1 sentence)
## Must-Have Requirements
- REQ-1: <summary> | AC count: N
## Out of Scope (explicit)
## Key Constraints
- Tech stack: (from s1-lock-tech-stack)
- Performance targets: (from REQ acceptance criteria)
- Security requirements: (from RULES.md)
## Forbidden Actions for All Downstream Agents
- Do NOT modify files outside scope
- Do NOT add dependencies not in locked tech stack
- Do NOT skip acceptance criteria
## Source Documents
- Vision: docs/specs/YYYY-MM-DD-<topic>-vision.md
- Requirements: docs/specs/YYYY-MM-DD-<topic>-requirements.md
- Rules: RULES.md
- Context: CONTEXT.md
```

### Step 3 — Commit
**Run**: `git add CONTEXT_SNAPSHOT.md && git commit -m "docs: add context snapshot"`
Notify: *"Context Snapshot committed. Stage 3 ready."*

---

## Completion Report

Report status using exactly one of:
- **DONE** — `CONTEXT_SNAPSHOT.md` committed; all source documents committed. Ready for Stage 3.
- **DONE_WITH_CONCERNS** — committed, but note any "Should-Have" requirements that may be cut if Stage 3 reveals complexity.
- **BLOCKED** — structured requirements not yet committed; cannot generate snapshot.
- **NEEDS_CONTEXT** — state exactly what is missing from upstream stages.

</what-to-do>

<supporting-info>

## Artifact Standard
`CONTEXT_SNAPSHOT.md` at project root, ≤50 lines, with `## Forbidden Actions` section and source document paths.

## Artifact Dependencies
- **Reads**: `docs/specs/YYYY-MM-DD-<topic>-requirements.md`, CONTEXT.md, RULES.md
- **Writes**: `CONTEXT_SNAPSHOT.md`

→ Full reference: `references/detail.md`

</supporting-info>
