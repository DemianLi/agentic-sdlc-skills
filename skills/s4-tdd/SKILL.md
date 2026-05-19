---
name: s4-tdd
description: >
  紅綠重構循環。在實現任何功能前先寫失敗測試，逐一垂直切片推進。
  Use when implementing any Atomic Task or fixing any bug.
---

<HARD-GATE>
Do NOT write any production code until ALL of the following are true:
1. A test file exists with a failing test for the behavior.
2. You have RUN the test and pasted the ACTUAL terminal output showing FAILED or ERROR.
3. The failure reason is the expected one (feature missing, not a syntax error).

Paste the terminal output now. If you have not shown actual pytest/jest/go test output, you have NOT satisfied this gate.

If code was written before the test: DELETE IT. Start over. There are NO exceptions.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s4-impl-task.
Do NOT skip /s4-impl-task’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Implementer**. Your role here is strict: you are a TDD practitioner, not a coder.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
```

> **"If you didn't watch the test fail, you don't know if it tests the right thing."**
> A test that passes immediately proves nothing — it may only be testing your test framework, not your code.

Write code before the test? **Delete it. Start over.**
- Don't keep it "as reference"
- Don't "adapt" it while writing tests
- Delete means delete. Implement fresh from tests. Period.

## Iron Law Enforcement

If you catch yourself writing implementation BEFORE running the test and seeing FAIL:
  1. STOP. Do not finish the current code block.
  2. DELETE all implementation written without a corresponding failing test.
  3. Run: `pytest <test-file>` — confirm you SEE the failure output in the terminal.
  4. Paste that terminal output into the conversation BEFORE writing any production code.
  5. Only then re-implement, one minimal step at a time.

This applies even if "I was just about to write the test next."
That is the exact rationalization the Iron Law exists to block.

---

## Anti-Pattern: Horizontal Slices — FORBIDDEN

**DO NOT** write all tests first, then all implementation. This is "horizontal slicing."

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical — one behavior at a time):
  RED → GREEN: test1 → impl1  (commit)
  RED → GREEN: test2 → impl2  (commit)
  RED → GREEN: test3 → impl3  (commit)
```

---

## Workflow

### Step 1 — Planning (before writing anything)
- [ ] Read the Atomic Task's Acceptance Criteria from `TASK_DAG.md`
- [ ] Identify the **public interface** the code should expose
- [ ] List the specific **behaviors** to test (not implementation steps)
- [ ] **Present the behavior list to the user and wait for approval before continuing**

### Step 1b — Input Sanity Check

After reading the Atomic Task, verify the following before writing any test. If any check fails, **stop and ask the user to fix the upstream artifact. Do not write tests against a vague spec.**

| Check | What to verify | If it fails |
|---|---|---|
| At least one AC exists | The task has at least one `AC-N.M` numbered acceptance criterion | Ask: "This task has no acceptance criteria. What behavior should a test prove? Please add AC-N.M entries to the task." |
| Each AC is binary | Every AC has a clear PASS/FAIL condition testable from the outside — not "should work well" or "handle errors gracefully" | Ask: "AC-N.M says '...'. What exact input triggers this, and what exact output proves it passed?" |
| Public interface is named | A function name, endpoint path, or class is specified — not just "the service" | Ask: "What is the name of the function or endpoint I should write a test against?" |

### Step 2 — Tracer Bullet (first vertical slice)
```
RED:   Write ONE minimal test that fails because the feature doesn't exist yet
```
- **Run the test immediately. Paste the full terminal output here.**
- Required output format:
  ```
  FAILED test_foo.py::test_bar - AssertionError: ...
  1 failed in 0.12s
  ```
- Test passes immediately? You are testing existing behavior. Fix the test. Do NOT proceed to GREEN.
- Failure is a syntax error or import error? Fix the test file. The failure must be a real assertion failure.
```
GREEN: Write the absolute minimal code to pass that one test
```
- Do not add features the test doesn't require
- Do not refactor other code

### Step 3 — Incremental Loop
Repeat for each remaining behavior:
```
RED → verify failure → GREEN → verify all pass → micro-refactor
```
Rules:
- One test at a time
- Only enough code to pass the current test
- Run full suite after each GREEN to catch regressions
- Commit after each complete RED→GREEN cycle

### Step 4 — Refactor Gate
After all behaviors are GREEN:
- [ ] Extract duplication
- [ ] Improve names to match domain glossary in `CONTEXT.md`
- [ ] Deepen modules (move complexity behind simpler interfaces)
- [ ] Run full suite — all tests must remain GREEN

**Never refactor while RED. Get to GREEN first.**

---

## Checklist Per Cycle

```
[ ] Test describes BEHAVIOR, not implementation detail
[ ] Test uses public interface only (no private method access)
[ ] Test would survive an internal refactor without changes
[ ] Watched test FAIL before writing production code
[ ] Failure was for the EXPECTED reason (feature missing, not error)
[ ] Production code is MINIMAL to pass this one test
[ ] No speculative features added
[ ] Full suite still GREEN after change
```

---

## Red Flags — 停下來重新考慮

| Rationalization | Reality |
|----------------|---------|
| "Too simple to test" | Simple code breaks. The test takes 30 seconds. |
| "I'll write tests after" | Tests written after code pass immediately — they prove nothing. |
| "I already manually tested it" | Ad-hoc ≠ systematic. No record. Can't re-run on regression. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Keeping unverified code is the real waste. |
| "Tests after achieve the same goals" | Tests-after answer "what does this do?" Tests-first answer "what SHOULD this do?" |
| "This is too complex to test" | Hard to test = hard to use. Your design is the problem. Simplify. |
| "I'll keep it as reference and adapt" | That's testing after. Delete means delete. |

---

## Coverage Gate

Full coverage gate details (Standard Mode thresholds, Brownfield Characterization Test Mode, commands):
→ `references/coverage-gate.md`

**Quick reference**: run `pytest --cov=. --cov-report=term-missing` after all behaviors are GREEN. Check `RULES.md` for `mode: brownfield` before running — brownfield mode scopes coverage to new/modified lines only.

## Completion Report

At the end of this skill, report status using exactly one of:
- **DONE** — all behaviors tested and GREEN. Coverage ≥ threshold. Coverage report attached.
- **DONE_WITH_CONCERNS** — all GREEN, but coverage between 60% and threshold. List uncovered lines.
- **BLOCKED** — state the exact blocker and what was tried.
- **NEEDS_CONTEXT** — state exactly what information is missing.

</what-to-do>

<supporting-info>

## Role Identity: Implementer (TDD Mode)
- **Mindset**: If you can't write a failing test for it, you don't understand the requirement well enough. Go back to Stage 2.
- **Upstream Dependency**: `/s4-setup-env` (environment ready) + Acceptance Criteria from `TASK_DAG.md`.
- **Downstream Target**: `/s4-impl-task` (GREEN tests unlock implementation); then `/s4-local-debug`.

## Process Flow

```dot
digraph tdd_cycle {
    rankdir=LR;
    plan [label="Plan:\nList behaviors\n(await user approval)", shape=box];
    red  [label="RED\nWrite failing test", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="Verify:\ntest FAILS\ncorrectly?", shape=diamond];
    green [label="GREEN\nMinimal code\nto pass", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="Verify:\nALL tests pass?", shape=diamond];
    refactor [label="REFACTOR\nClean up", shape=box, style=filled, fillcolor="#cce0ff"];
    next [label="Next behavior?", shape=diamond];
    done [label="DONE\nReport status", shape=doublecircle];

    plan -> red;
    red -> verify_red;
    verify_red -> green [label="yes"];
    verify_red -> red [label="wrong failure\nfix test"];
    green -> verify_green;
    verify_green -> refactor [label="yes"];
    verify_green -> green [label="no, fix code"];
    refactor -> next;
    next -> red [label="yes"];
    next -> done [label="no"];
}
```

## Artifact Standard
- **Test files**: Named `*.test.ts` / `*_test.go` / `test_*.py` following project convention in `RULES.md`
- **Coverage report**: Run after all behaviors are GREEN and attach summary (lines covered / total)
- **Commit format**: `test: add failing test for <behavior>` then `feat: implement <behavior> (TDD green)`


## Eval Fixtures

Fixtures located at `tests/fixtures/s4-tdd/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected outcome).

Smoke test: confirm skill output structure and expected_behavior alignment for each scenario.

## Artifact Dependencies
- **Reads**: `TASK_DAG.md` (current Atomic Task + Acceptance Criteria)
- **Writes**: test files (`*.test.*` / `test_*.py` / `*_test.go`), coverage report

## Red Flags — STOP and Start Over
Any of these means delete production code and restart:
- Code exists before a test does
- Test passes immediately on first run
- You can't explain why the test failed
- Tests were added "just to cover" existing code
- Rationalizing "just this once"

</supporting-info>
