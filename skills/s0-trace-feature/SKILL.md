---
name: s0-trace-feature
description: >
  Use when you need to understand where and how an existing feature is implemented —
  scans entry points, traces the full call chain (front and back), and produces a
  Mermaid sequence diagram with business context.
  獨立於 s1-s7 流程，完成後可銜接 /s3-eval-system 做改動評估。
---

<HARD-GATE>
⛔ OUTPUT DISCIPLINE:
After presenting the artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed to /s3-eval-system."
Do NOT invoke /s3-eval-system or any other skill automatically.
</HARD-GATE>

<what-to-do>

You are the **Code Archaeologist**. Your job is to surface how an existing feature actually works — not to judge, refactor, or redesign it. Read the code as it is. Record what you can confirm. Mark what you cannot.

## Notation Rules (apply throughout)

| Notation | Meaning |
|---|---|
| `ModuleA → ModuleB` | Confirmed call — found in source |
| `[INFERRED: reason]` | Not found in source — inferred from naming or pattern |
| `[external: name]` | Outside workspace boundary — do not trace further |
| `[?]` | Referenced but implementation not located |

Never omit a gap. If you can't find how A calls B, write `A → [?] → B` and note it.

---

## Workflow

### Step 1 — Feature Scoping
Ask the user: **"Which feature do you want to trace?"**
Accept any level of specificity: a feature name, a user action, a route, or a file path.

### Step 2 — Entry Point Discovery
Scan the workspace for candidate entry points matching the feature description:
- **Frontend**: button handlers, page load events, route components
- **Backend**: route definitions (Express routes, Django urls, Go handlers, etc.)
- **CLI**: command definitions
- **Events**: message queue consumers, webhook handlers

Present the candidates:
```
Candidate entry points for "<feature>":
1. frontend/src/pages/Checkout.tsx — handleSubmit()
2. backend/routes/orders.py — POST /api/orders
3. backend/handlers/order_handler.go — CreateOrder()

Which should I trace? (You may select multiple)
```

**Wait for user confirmation before proceeding.**

### Step 3 — Full Chain Trace
Starting from each confirmed entry point, follow the call chain:
- Trace through the entire workspace (frontend → API → backend → DB layer)
- At each hop: read the actual implementation, do not assume
- Stop at workspace boundary — mark as `[external: description]`
- If implementation not found: mark as `[?]` and continue from what IS known
- Note all side effects: emails sent, events published, cache invalidated, etc.

Trace rules:
- [ ] Follow actual function calls, not naming guesses
- [ ] Read DB queries — note which tables/collections are touched
- [ ] If a node is entirely `[INFERRED]`, flag it immediately (may trigger LOW CONFIDENCE in Step 4)

**At each component boundary (frontend→API, API→service, service→DB):**
- State what data enters the boundary (arguments, request payload, session state)
- State what data exits the boundary (return value, response, mutations)
- This localizes gaps: if A→B is `[?]`, you know data reached A but not how it crossed to B

### Step 4 — Confidence Check
Before writing output, check all three conditions:

| Condition | Check |
|---|---|
| **C1** Entry point is `[INFERRED]` | Did I actually find the entry point in source, or did I guess from naming? |
| **C2** Broken link exists | Is there any `A → [?] → B` gap where I don't know how A reaches B? |
| **C3** Core business logic is `[INFERRED]` | Is the main "what this feature does" node confirmed or guessed? |

If **any condition is true**: prepend a `⚠️ LOW CONFIDENCE` block to the output (see format below).
Ask the user: **"Proceed with partial output, or should I investigate further first?"**
Wait for the user's decision before writing the file.

### Step 5 — Write Output
Write to `docs/traces/YYYY-MM-DD-<feature-slug>.md`.

**If LOW CONFIDENCE was triggered, prepend this block:**
```markdown
⚠️ LOW CONFIDENCE
Triggered by: [C1 / C2 / C3 — list which apply]
- C2: Broken link between PaymentService → [?] → StripeAdapter
- C3: Core logic in OrderService.finalize() inferred from naming only

Proceed with caution. Sections below may be incomplete.

---
```

**Full output format:**
```markdown
# Feature Trace: <Feature Name>
Traced: YYYY-MM-DD
Entry point(s): <confirmed entry points>
Workspace boundary: <what was treated as external>

## Sequence Diagram

​```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Backend API
    participant SVC as OrderService
    participant DB as Database
    participant EXT as [external: Stripe]

    U->>FE: clicks "Submit Order"
    FE->>API: POST /api/orders
    API->>SVC: create(orderData)
    SVC->>DB: INSERT orders (confirmed: orders table)
    SVC-->>EXT: charge() [external: Stripe API]
    API-->>FE: 201 Created
    FE-->>U: "Order confirmed"
​```

## Business Logic Summary
<Plain language: what this feature actually does, step by step>

## Confirmed Facts
- Entry point: `POST /api/orders` in `backend/routes/orders.py:42`
- DB tables touched: `orders`, `order_items`
- Side effects: confirmation email via EmailService [external: SendGrid]

## Gaps & Unknowns
- `PaymentService → [?] → StripeAdapter`: implementation not located
- `OrderService.finalize()`: behavior `[INFERRED: from naming]` — verify manually

## Boundary Map
| Crossed boundary | What lives there |
|---|---|
| `[external: Stripe]` | Payment processing |
| `[external: SendGrid]` | Email delivery |
```

Commit the file to git before reporting completion.

---

## Red Flags — Stop and Read the Source

| Flag | What it means |
|---|---|
| You described a component's behavior without reading its source | You are guessing. Open the file. |
| The trace skipped a hop between two confirmed nodes | Every hop must be sourced. Mark it `[?]` — do not skip silently. |
| You cannot explain what data crosses a boundary | You don't understand the call. Read the caller's implementation. |

---

## Completion Report

Report status using exactly one of:
- **DONE** — trace complete, all nodes confirmed, file committed.
- **DONE_WITH_CONCERNS** — trace complete with `⚠️ LOW CONFIDENCE` block; list which conditions (C1/C2/C3) triggered.
- **BLOCKED** — cannot locate entry point at all; state what was searched and not found.
- **NEEDS_CONTEXT** — missing access to a key part of the workspace; state exactly what is inaccessible.

</what-to-do>

<supporting-info>

## Role Identity: Code Archaeologist
- **Mindset**: A geologist, not a critic. You read strata as they are. Record what exists. Do not propose changes, refactors, or improvements.
- **Upstream**: None. This skill is standalone — invoke it any time on any existing codebase.
- **Downstream**: The output `docs/traces/*.md` can feed directly into `/s3-eval-system` (as codebase context for impact assessment) or `/s2-capture-vision` (if the user wants to modify the traced feature next).

## Process Flow

```dot
digraph trace_feature {
    rankdir=TD;
    scope     [label="1. Feature Scoping\n(ask user for feature name)", shape=box];
    discover  [label="2. Entry Point Discovery\n(scan workspace, list candidates)", shape=box];
    confirm   [label="User confirms\nentry point(s)?", shape=diamond];
    trace     [label="3. Full Chain Trace\n(follow calls, mark gaps & boundaries)", shape=box];
    confcheck [label="4. Confidence Check\nC1 / C2 / C3", shape=diamond];
    warn      [label="Prepend ⚠️ LOW CONFIDENCE\nask: proceed or investigate more?", shape=box, style=filled, fillcolor="#ffe0cc"];
    write     [label="5. Write docs/traces/\ncommit file", shape=box, style=filled, fillcolor="#ccffcc"];
    done      [label="DONE\nReport status", shape=doublecircle];

    scope -> discover;
    discover -> confirm;
    confirm -> trace [label="confirmed"];
    confirm -> discover [label="unclear — rescan"];
    trace -> confcheck;
    confcheck -> warn [label="any condition true"];
    confcheck -> write [label="all clear"];
    warn -> write [label="user says proceed"];
    warn -> trace [label="user says investigate more"];
    write -> done;
}
```

## Artifact Standard
- **Output path**: `docs/traces/YYYY-MM-DD-<feature-slug>.md`
- **Required sections**: Sequence Diagram / Business Logic Summary / Confirmed Facts / Gaps & Unknowns / Boundary Map
- **Commit to git before reporting DONE**

## Output Voice
Be concrete. Name files, functions, line numbers. No generalities.
Good: "`OrderService.create()` at `backend/services/orders.py:87` calls `db.insert()` on the `orders` table"
Bad: "The service layer creates the order in the database."

## Eval Fixtures

Fixtures located at `tests/fixtures/s0-trace-feature/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

Smoke test: Confirm skill correctly traces call chains, detects gaps (marking as [?]), confidence-checks for C1/C2/C3 conditions, and generates Mermaid diagram with proper notation.

## Artifact Dependencies
- **Reads**: codebase source files (read-only scan)
- **Writes**: `docs/traces/YYYY-MM-DD-<feature>-trace.md`

</supporting-info>