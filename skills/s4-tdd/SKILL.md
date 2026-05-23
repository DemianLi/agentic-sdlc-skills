---
name: s4-tdd
description: >
  Use when implementing any Atomic Task or fixing any bug — outputs test files and
  coverage report. NOT for tasks without Acceptance Criteria in TASK_DAG.md.
---

<HARD-GATE>
Do NOT write any production code until ALL of the following are true:
1. A failing test exists for the behavior.
2. You HAVE RUN the test — paste ACTUAL terminal output showing FAILED or ERROR.
3. Failure reason is expected (feature missing, not a syntax error).

No output shown = gate not satisfied. Code written before the test: DELETE IT. No exceptions.

---
⛔ After completing this skill: proceed immediately to /s4-impl-task.
</HARD-GATE>

<what-to-do>

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
> "If you didn't watch the test fail, you don't know if it tests the right thing."

Write code before the test? Delete it. Not "as reference". Not "adapted". Delete means delete.

**FORBIDDEN — Horizontal Slices**: NOT `test1+test2+test3 → impl1+impl2+impl3`. CORRECT: `(test1→impl1→commit)` repeat.

---

## Workflow

### Step 1 — Planning
- [ ] Read Atomic Task's Acceptance Criteria from `TASK_DAG.md`
- [ ] Identify the **public interface** the code should expose
- [ ] List specific **behaviors** to test (not implementation steps)
- [ ] **Present behavior list to user — wait for approval before continuing**

### Step 1b — Input Sanity Check
Verify before any test: (1) ≥1 `AC-N.M` criterion exists; (2) each AC has binary PASS/FAIL testable from outside; (3) public interface (function/endpoint/class name) specified. Any fail → ask user to fix first.

### Step 2 — Tracer Bullet
```
RED: Write ONE minimal failing test — run it — paste terminal output
```
Required: `FAILED test_foo.py::test_bar - AssertionError... / 1 failed in 0.12s`
- Test passes immediately → testing existing behavior; fix the test
- Failure is syntax/import error → fix test file; must be a real assertion failure
```
GREEN: Absolute minimal code to pass that one test. No extra features. No refactoring.
```

### Step 3 — Incremental Loop
Repeat: `RED → verify failure → GREEN → verify all pass → micro-refactor → commit`

### Step 4 — Refactor Gate (after all GREEN)
- [ ] Extract duplication; improve names per `CONTEXT.md` glossary
- [ ] Full suite must remain GREEN. **Never refactor while RED.**

---

## Checklist Per Cycle

```
[ ] Test describes BEHAVIOR, not implementation detail
[ ] Test uses public interface only (no private method access)
[ ] Test would survive an internal refactor without changes
[ ] Watched test FAIL before writing production code
[ ] Failure was for the EXPECTED reason
[ ] Production code is MINIMAL to pass this one test
[ ] No speculative features added
[ ] Full suite still GREEN after change
```

---

## Red Flags

| Rationalization | Reality |
|----------------|---------|
| "I'll write tests after" | Tests after pass immediately — prove nothing. |
| "Deleting X hours of work is wasteful" | Sunk cost. Unverified code is the real waste. |
| "Tests after achieve the same goals" | After: "what does this do?" First: "what SHOULD this do?" |
| Code exists before test / passes immediately / can't explain failure | DELETE and restart |

## Coverage Gate
→ `references/coverage-gate.md`. Quick ref: `pytest --cov=. --cov-report=term-missing`
## Completion Report
- **DONE** — all behaviors GREEN; coverage ≥ threshold; coverage report attached.
- **DONE_WITH_CONCERNS** — all GREEN; coverage 60%–threshold; list uncovered lines.
- **BLOCKED** — state exact blocker and what was tried.
- **NEEDS_CONTEXT** — state exactly what information is missing.

</what-to-do>

<supporting-info>

## Artifact Dependencies
- **Reads**: TASK_DAG.md (Atomic Task + Acceptance Criteria)
- **Writes**: test files (`*.test.*` / `test_*.py` / `*_test.go`), coverage report
- **Commit format**: `test: add failing test for <behavior>` → `feat: implement <behavior> (TDD green)`

→ Full reference: `references/detail.md`

</supporting-info>
