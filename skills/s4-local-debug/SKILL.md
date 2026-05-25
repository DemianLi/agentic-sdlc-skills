---
name: s4-local-debug
description: >
  Use when diagnosing build failures or behavior mismatches with evidence-based
  debugging. Outputs fix + regression test. NOT for writing new tests (use s4-tdd).
---

<HARD-GATE>

Do NOT apply any fix until root cause is confirmed via INSTRUMENT phase and fix is committed with regression test.

After presenting the required artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed to Stage 5 Code Auditor."
</HARD-GATE>

<what-to-do>

You are the **Implementer** in debug mode. Diagnose and fix failures using disciplined, evidence-based investigation. Never guess. Never fix without understanding.

### Phase 1 — REPRODUCE
- [ ] Run: `npm test` / `go test ./...` / `pytest`; confirm consistent; document verbatim.
- [ ] Identify: **build**, **runtime**, or **test failure**?
Stop if not reproducible: `NEEDS_CONTEXT: intermittent — cannot diagnose.`

### Phase 2 — MINIMISE
- [ ] Smallest input/path triggering failure; remove unrelated code; confirm which assertion fails first.

### Phase 2.5 — ANALOGY
Find working counterpart; diff side-by-side (data flow? error handling? init order?). List every difference as hypothesis. (95% of "unsolvable" bugs = incomplete investigation.)

### Phase 3 — HYPOTHESISE
Write: *"Root cause is _____ because _____."* List file/function/line suspected.

### Phase 4 — INSTRUMENT
Add `console.log` / `fmt.Printf` at suspected location. Collect actual vs. expected. Cross-reference stack trace.

### Phase 5 — FIX
Change only what addresses root cause. NO refactoring. NO features. Remove all instrumentation.

### Phase 6 — REGRESSION TEST
Write failing test **before** fix. Watch it fail. Apply fix. Confirm GREEN. Commit: `fix: <root cause> (+ regression test)`. Bug without test = time bomb.

→ Error type triage: `references/s4-local-debug-error-triage.md`

**Escalation**: After 3 failed attempts: STOP. Report `BLOCKED: attempted [X], [Y], [Z]`. Ask: escalate?

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| "Failure is obvious, logic wrong, just fix — no INSTRUMENT needed" | "Obvious" assumptions fail most; no data = guessing; need logs + stack trace evidence |
| "3 hypotheses failed but 4th is very likely, try once more" | 3 attempts is hard limit; 4th means you don't truly understand; STOP, report BLOCKED, seek help |
| "Regression test is complex, I'll submit fix first, add test later" | Fix + test are inseparable; fix without test = time bomb; test first (RED), watch fail, then fix |

## Completion Report

- **DONE** — root cause identified, fix applied, regression test added, full suite GREEN.
- **DONE_WITH_CONCERNS** — fixed, but note specific risks (e.g., "similar pattern in module X").
- **BLOCKED** — state exact blocker, what was tried (all 3 attempts), what is needed.
- **NEEDS_CONTEXT** — state exactly what information is missing.
</what-to-do>

<supporting-info>

**Reads**: failing test output, source files
**Writes**: bug fix commits, regression test

## Eval Fixtures

Fixtures located at `tests/fixtures/s4-local-debug/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
