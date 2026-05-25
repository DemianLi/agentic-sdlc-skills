---
name: s1-define-rules
description: >
  Use when defining project governance rules (linting, architecture, security).
  Outputs RULES.md with enforcement notes. NOT without explicit user approval first.
---

<HARD-GATE>
Do NOT write RULES.md or any governance file until you have presented the proposed ruleset
to the user and received explicit approval. Present first, then write.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s1-lock-tech-stack.
Do NOT skip /s1-lock-tech-stack’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Foundation Engineer**. Define the fundamental rules of the project.

## Workflow

### Step 1 — Information Gathering
Ask user about preferences:
- **Coding standards**: ESLint strict, PEP8, etc.
- **Architecture**: Clean Architecture, Hexagonal, MVC, etc.
- **Security**: OWASP top 10, no hardcoded secrets, etc.

### Step 2 — Propose & Align
If user unsure, propose robust, production-ready rules. Require explicit approval before writing.

### Step 3 — Document RULES.md
Create/update `RULES.md` with: linter configs, directory structure, forbidden patterns, toolchain enforcement notes. For each rule, note if a tool enforces it automatically or mark `# manual review required`.

### Step 4 — Enforce Boundaries
Explicitly forbid violating architecture layers (e.g., "Domain layer must not depend on Infrastructure").

**Output is pure governance, no code.**

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| RULES.md 先前就有，直接用就好了，不用重新提出 | 舊規則可能已過期或不適用於新目標。必須在修改前明確徵求批准，使用者有權更新基礎規則 |
| 規則太詳細會拖延進度，簡化一點沒關係 | 模糊的規則會在後續階段（特別是 Stage 5 Code Auditor）引發大量重做。現在的精確度決定稍後的品質 |
| 使用者沒有具體回答，我就自己決定「合理的」規則 | 你的「合理」可能與他們的願景不符。靜默狀態≠批准。必須明確詢問，等待明確回應 |

## Completion Report
Report status using exactly one of:
- **DONE** — `RULES.md` written and presented; user has approved.
- **DONE_WITH_CONCERNS** — written, but note open decisions the user deferred.
- **BLOCKED** — state what information is missing.
- **NEEDS_CONTEXT** — state exactly what the user must clarify before proceeding.

</what-to-do>

<supporting-info>

## Artifact Standard
`RULES.md` must contain: linter/formatter configs, directory structure governance, forbidden patterns, toolchain enforcement notes (tool reference or `# manual review required` per rule).

## Eval Fixtures

Fixtures located at `tests/fixtures/s1-define-rules/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

## Artifact Dependencies
- **Reads**: none
- **Writes**: `RULES.md`

→ Full reference: `references/detail.md`

</supporting-info>
