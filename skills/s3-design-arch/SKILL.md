---
name: s3-design-arch
description: >
  Use after /s3-eval-system to produce the OpenSpec design document (data structures,
  API contracts, sequence diagrams) before decomposing tasks.
---

<HARD-GATE>
Do NOT proceed to `/s3-breakdown-wbs` until:
1. The OpenSpec design document has been written and COMMITTED to git.

A design that exists only in memory is not an artifact; it is an intention.
`/s3-breakdown-wbs` reads `docs/arch/YYYY-MM-DD-<topic>-design.md` — if that file
does not exist on disk and in git, the next stage has nothing to read and cannot start.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s3-breakdown-wbs.
Do NOT skip /s3-breakdown-wbs’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **System Architect** in design mode. Your output is a contract — every downstream implementer (Stage 4) and auditor (Stage 5) will hold you to exactly what you write here.

## Design Document Format (OpenSpec Standard)

Create `docs/arch/YYYY-MM-DD-<topic>-design.md` with the following sections:

---

### Section 1 — Context
```markdown
## Context

**Problem**: <One sentence: what problem does this design solve?>
**Constraints**: <list constraints from RULES.md and tech stack>
**Assumptions**: <explicitly state what you are assuming to be true>
```

### Section 2 — Decision
```markdown
## Decision

**Chosen Approach**: <title of the selected approach>

**Rationale**: <why this approach over alternatives>

**Rejected Alternatives**:
- **Option A** — rejected because <reason>
- **Option B** — rejected because <reason>
```

### Section 3 — Data Structures & Schemas
Define every data model involved:
```typescript
// Example — use the actual project language
interface Order {
  id: string;           // UUID v4
  status: OrderStatus;  // enum defined below
  items: OrderItem[];
  createdAt: Date;      // ISO 8601 UTC
}

enum OrderStatus { PENDING = 'pending', CONFIRMED = 'confirmed', CANCELLED = 'cancelled' }
```

### Section 4 — API Contracts
For every new or modified endpoint, define:
```markdown
### POST /api/orders

**Request**:
```json
{ "customerId": "uuid", "items": [{ "productId": "uuid", "quantity": 1 }] }
```

**Response (200)**:
```json
{ "orderId": "uuid", "status": "pending", "createdAt": "2024-01-01T00:00:00Z" }
```

**Error Responses**:
- 400: `{ "error": "INVALID_ITEMS", "detail": "..." }`
- 409: `{ "error": "OUT_OF_STOCK", "productId": "uuid" }`
```

### Section 5 — Sequence Diagrams (Mermaid)
At minimum, illustrate the primary happy path:

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant OrderService
    participant DB

    Client->>API: POST /api/orders
    API->>OrderService: createOrder(items)
    OrderService->>DB: INSERT order
    DB-->>OrderService: orderId
    OrderService-->>API: Order{id, status: PENDING}
    API-->>Client: 201 Created
```

Add additional diagrams for error flows and critical edge cases.

### Section 6 — Consequences
```markdown
## Consequences

**Positive**:
- <what this design makes easier>

**Negative / Trade-offs**:
- <what this design makes harder or forecloses>

**Risks**:
- <identified technical risks and mitigation strategy>
```

### Section 7 — Delta Spec (OpenSpec)
Track exactly what this design changes at the component level. Use the Change ID as the traceability anchor for Stage 3 tasks and Stage 5 audits.

```markdown
## Delta Spec

**Change ID**: `<kebab-case-feature-name>` (e.g., `user-auth-jwt`, `order-cancellation-flow`)

### Added
- `ComponentA`: <new behavior or interface added>

### Modified
- `ComponentB`: <what changes and why the old behavior was insufficient>

### Removed
- `ComponentC`: <what is deleted and confirmation it has no remaining callers>

### Unchanged (explicitly verified)
- `ComponentD`: <confirmed unaffected — no changes required>
```

---

## Workflow

1. Read `docs/arch/YYYY-MM-DD-<topic>-impact.md` from `/s3-eval-system`
2. Read `RULES.md` — the design MUST conform to the architectural paradigm defined there

**Step 2b — Input Sanity Check**

After reading the impact report, verify the following before writing any design section. If any check fails, **stop and state exactly what is missing. Do not begin writing.**

| Check | What to verify | If it fails |
|---|---|---|
| Impact report names specific files | At least one source file path is listed — not just "the service layer" or "the order module" | Ask: "Which specific files are affected? Please update the impact report with exact paths before I design." |
| Breaking changes are explicit | Each 🔴 item states what contract changes and how — not just "might break" | Ask: "For breaking change '...', what exactly changes — a field name, response schema, or function signature?" |
| `## Recommended Approach` exists | The impact report gives a direction for the design | If absent, proceed but explicitly note the missing direction in the design's `## Context` section and ask the user to confirm the approach before continuing. |

3. Write each section of the design document
4. Present to user **section by section** — ask for approval after each section before continuing
5. After all sections approved, commit and proceed

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "我已經在代碼中看到類似的模式，設計應該是一致的" | 設計文件必須獨立自 RULES.md 和影響報告；不能靠「我假設代碼已經對了」 |
| "用戶對粗略版本的序列圖點頭，細節可以 s4 再調整" | Mermaid 圖是 s3-breakdown-wbs 拆解任務的依據；細節變更必須重新呈現 |
| "OpenSpec 還沒完全寫完，但 API schema 核心部分已經 OK 了" | 「還沒完成」= 還沒提交；不能分部分批准 |

---

## Completion Report

Report status using exactly one of:
- **DONE** — OpenSpec written, all sections approved, committed. Proceeding to `/s3-breakdown-wbs`.
- **DONE_WITH_CONCERNS** — approved with reservations; list open architectural questions.
- **BLOCKED** — design conflicts with an existing ADR or RULES.md constraint; state the conflict.
- **NEEDS_CONTEXT** — state exactly what technical information is missing.

</what-to-do>

<supporting-info>

## Role Identity: System Architect (Design Mode)
- **Mindset**: Contract-first design. If it isn't written and approved, it doesn't exist. Structural elegance and interface minimalism — the best modules are deep (simple interface, rich behavior).
- **Upstream Dependency**: `/s3-eval-system` impact report; `RULES.md` architectural paradigm.
- **Downstream Target**: `/s3-breakdown-wbs` uses the API contracts and data schemas to define Atomic Tasks; Stage 4 implements against this document; Stage 5 audits against it.

## Process Flow

```dot
digraph design_arch {
    rankdir=TD;
    load    [label="1. Load Impact Report\n+ RULES.md constraints", shape=box];
    ctx     [label="2. Write Section 1: Context\n(problem / constraints / assumptions)", shape=box];
    ctx_ok  [label="User approves\nContext?", shape=diamond];
    dec     [label="3. Write Section 2: Decision\n(approach / rationale / rejected alts)", shape=box];
    dec_ok  [label="User approves\nDecision?", shape=diamond];
    data    [label="4. Write Section 3: Data Structures\n(typed schemas)", shape=box];
    api     [label="5. Write Section 4: API Contracts\n(req / res / errors per endpoint)", shape=box];
    seq     [label="6. Write Section 5: Sequence Diagrams\n(Mermaid — happy path + error flows)", shape=box];
    cons    [label="7. Write Section 6: Consequences\n(positive / negative / risks)", shape=box];
    approve [label="User approves\nfull document?", shape=diamond];
    done    [label="DONE\nCommit + proceed to /s3-breakdown-wbs", shape=doublecircle];
    blocked [label="BLOCKED\nConflicts with ADR\nor RULES.md", shape=doublecircle];

    load -> ctx;
    ctx -> ctx_ok;
    ctx_ok -> dec [label="yes"];
    ctx_ok -> ctx [label="no, revise"];
    dec -> dec_ok;
    dec_ok -> data [label="yes"];
    dec_ok -> dec [label="no, revise"];
    data -> api -> seq -> cons;
    cons -> approve;
    approve -> done [label="yes"];
    approve -> blocked [label="conflict unresolvable"];
}
```

## Artifact Standard
Output file: `docs/arch/YYYY-MM-DD-<topic>-design.md`

Required sections (all mandatory):
1. `## Context` — problem, constraints, assumptions
2. `## Decision` — chosen approach, rationale, rejected alternatives
3. `## Data Structures` — typed schemas for every model
4. `## API Contracts` — every endpoint with request/response/error schemas
5. `## Sequence Diagrams` — Mermaid diagram for happy path (minimum)
6. `## Consequences` — positive, negative, risks

Commit before transitioning.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s3-design-arch/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Artifact Dependencies
- **Reads**: `docs/arch/YYYY-MM-DD-<topic>-impact.md`, `RULES.md`
- **Writes**: `docs/arch/YYYY-MM-DD-<topic>-design.md`

</supporting-info>
