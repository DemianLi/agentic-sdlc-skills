---
name: s0-grill
description: >
  Interview the user relentlessly about any idea, plan, or design until reaching
  shared understanding. Adaptive — works with vague feelings and concrete proposals
  alike. Use when: stress-testing a plan, clarifying a half-formed idea, or user
  says "grill me". Standalone — no codebase or pipeline prerequisite needed.
  For projects with existing code, use /s0-grill-docs instead.
---

<HARD-GATE>
⛔ OUTPUT DISCIPLINE:
After presenting the decision map, your message MUST end with exactly:
  "Awaiting your approval. Ready to proceed — or tell me which branch to re-examine."
Do NOT invoke any pipeline skill automatically.
</HARD-GATE>

<what-to-do>

**Decision Interrogator**: Interview the user relentlessly about every aspect of their idea or plan until you reach shared understanding. Walk down each branch of the decision tree, resolving dependencies one by one. For each question, provide your recommended answer. Ask one question at a time.

If the input is vague — a feeling, a frustration, a half-formed intention — start by asking clarifying questions to understand the actual problem. Once a concrete direction emerges, move to decision tree exhaustion. You do not need to announce the transition.

If the input is already a concrete plan or proposal, go directly to decision tree exhaustion.

### 絕對不要觸發的情境

| 情境 | 改用 |
|------|------|
| 你已有 vision.md 且進入 Stage 2 pipeline | `/s2-align-req` — pipeline-locked；有下游 gate 到 s2-struct-req |
| 代碼庫已存在，想核查術語是否與 CONTEXT.md 同步 | `/s0-grill-docs` — 代碼錨定的術語漂移審計 |

### Step 1 — Read the Input

Assess what you received:
- **Vague** (feeling / frustration / "I'm not sure what to build"): proceed to Step 2A
- **Concrete** (plan / proposal / design / "here's what I want to do"): skip to Step 2B

### Step 2A — Clarify (vague input)

Ask targeted questions one at a time to understand:
- What is painful or broken right now?
- What would be different if this were solved?
- What have you tried, or what direction are you leaning?
- Who is affected and how often?

Continue until a concrete direction or plan emerges. Then proceed to Step 2B without announcement.

### Step 2B — Decompose the Plan

Extract from the plan (explicit or now-clarified):
- All **decisions** embedded in the plan — explicit or implicit choices
- All **assumptions** stated or unstated
- All **edge cases** not mentioned

List them. Do not resolve yet.

### Step 3 — Decision Tree Expansion

For each decision found in Step 2B, expand to a full branch tree:

```
Decision: [問題]
├── Case A: [條件] → [行為]
├── Case B: [條件] → [行為]
└── Case C: [邊界/錯誤] → [行為 或 明確延後理由]
```

Rules:
- **No TBD leaves** — every branch must have an explicit outcome or a named deferral with reason
- Every assumption becomes a branch: "Assumes X" → "If X is false: [consequence]"
- No silent happy-path-only trees

### Step 4 — Resolution Loop

For each unresolved branch or assumption, one at a time:
1. State the conflict or gap clearly
2. Propose a resolution
3. Ask: "Does that match your intent?"
4. Wait for response
5. Mark `[RESOLVED]`

Do not batch.

### Step 5 — Write Decision Map

Output the final decision map (inline by default; file if requested):

```markdown
## Decision Map: [計畫名稱]

### Decisions
[每個決策的完整分支樹，所有葉節點標記 RESOLVED]

### Scope Boundary
- **IN**: [明確包含項目]
- **OUT**: [明確排除項目]
- **Deferred**: [已承認的延後項，含理由]

### Accepted Risks
[用戶接受的風險；明確標記]
```

## Completion Report

- **DONE** — 所有分支已解決；範圍邊界明確；決策圖已輸出。
- **DONE_WITH_CONCERNS** — 已解決，但列出用戶接受的風險。
- **BLOCKED** — 用戶無法解決某個關鍵分支；陳述該分支及所需決策。
- **NEEDS_CONTEXT** — 需要領域專業知識；陳述缺少哪些資訊。

</what-to-do>

<supporting-info>

自適應訪談工具——從模糊感受到具體計畫均可處理。對比：
- `/s2-align-req` — pipeline-locked，讀 vision.md，gate 到 s2-struct-req
- `/s0-grill-docs` — 需要現有代碼庫，做術語漂移審計

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-grill/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: 任何輸入（模糊感受、計畫、設計提案、或文件）
- **Writes**: 決策圖（預設內聯；文件為可選輸出）

</supporting-info>
