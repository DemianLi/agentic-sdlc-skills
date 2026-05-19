# Skill Eval — s4-impl-task — 2026-05-19

**File**: `skills/s4-impl-task/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ❌ FAIL | Lines 65–67: Upstream (`/s4-tdd`) and downstream (`/s4-local-debug`) named, but no adjacent s4-* skills compared; no explanation of how impl-task differs from tdd, debug, or optimize |
| 2 | 雙向阻斷 | ⚠️ PARTIAL | Lines 46–52: "Red Flags" list 3 implementation pitfalls, but no "Do NOT use this skill if" block; counter-examples describe code anti-patterns, not invocation scenarios |
| 3 | 輸入清洗 | ✅ PASS | Lines 23–35: Inputs explicitly listed (test file, TASK_DAG.md, RULES.md) with failure scenarios (missing test, missing AC, rules conflict) and defined behavior (BLOCKED, NEEDS_CONTEXT) |
| 4 | 漸進披露 | ✅ PASS | No large inline code blocks; implementation guidance is concise with clear step numbers |
| 5 | 優雅降級 | ⚠️ PARTIAL | Multiple file reads (test file, TASK_DAG.md, RULES.md) with no explicit fallback if read fails; lines 39–44 execute tests but no timeout or crash-recovery strategy defined |
| 6 | 漂移監控 | ✅ PASS | Line 71: References `tests/fixtures/s4-impl-task/cases.json`; fixture exists with 3 scenarios (simple implementation, rule conflict, scope discipline) |

**Total**: 3/6 PASS — **DRAFT**

## Defect Details

### ❌ FAIL — Criterion 1: 衝突防禦 (Semantic Anti-Collision)
- **Location**: Lines 65–67 (`<supporting-info>`)
- **Defect**: Downstream target is `/s4-local-debug`, but how does impl-task differ from it? When would a user invoke impl-task vs. tdd? The skill description (lines 4–5) says "after /s4-tdd has produced failing tests," but what if user has existing tests not written by s4-tdd? Does impl-task still apply?
- **Impact**: Routing confusion in a cluster of s4-* skills (tdd, impl-task, local-debug, setup-env). User could invoke wrong skill or invoke this one redundantly.

### ⚠️ PARTIAL — Criterion 2: 雙向阻斷 (Negative Triggers)
- **Location**: Lines 46–52
- **Gap**: "Red Flags" describe what NOT to do during implementation (refactor after green, modify out-of-scope files, pre-implement future tasks), but skill lacks explicit invocation anti-patterns. When should user NOT call this skill?
  - Missing example: "Do NOT use if all tests are already GREEN" (should go to s4-local-debug instead).
  - Missing example: "Do NOT use if TASK_DAG.md doesn't exist" (should be BLOCKED or ask user to run s3-build-dag first).

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Lines 39–44 (test execution)
- **Gap**: 
  - Test file read failures not handled; if file is unreadable, skill has no fallback.
  - Line 43: "run tests in loop until all tests GREEN" — what if test runner crashes, hangs, or times out? No timeout defined. No recovery strategy.
  - TASK_DAG.md updates (line 44) assume write succeeds; no rollback if update fails mid-way.
- **Impact**: Low blast-radius for reads, but high-impact for test execution hangs or file write corruption.

## Recommended Next Steps

1. Add explicit "Do NOT use if" section listing ≥2 invocation anti-patterns (e.g., "if tests are already green," "if TASK_DAG.md missing," "if user has not run /s4-tdd yet").
2. Define timeout for test loop (e.g., "if tests hang for >2 minutes, report BLOCKED and ask user to debug test suite manually").
3. Add try-catch for TASK_DAG.md write with fallback: if update fails, report BLOCKED and show user the exact line that failed.

This will address Criterion 1 (FAIL) and improve Criterion 2 & 5 to move skill toward NEAR READY.

