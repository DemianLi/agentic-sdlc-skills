# Skill Eval — s4-local-debug — 2026-05-19

**File**: `skills/s4-local-debug/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Lines 132–138: `<supporting-info>` names `/s4-impl-task` (upstream) and "Stage 5 (Code Auditor)" (downstream) with explicit "Implementer (Debug Mode)" identity |
| 2 | 雙向阻斷 | ✅ | Lines 8–18: `<HARD-GATE>` block with 1 hard condition; Lines 112–119: "Red Flags" table with 3 concrete anti-patterns (guessing without instrumentation, 4th attempt after 3 failures, uncommitted regression test) |
| 3 | 輸入清洗 | ⚠️ | Lines 88–98 "Quick Reference: Error Type Triage" lists failure types but no explicit input specification (what triggers this skill?) or defined behavior for intermittent failures |
| 4 | 漸進披露 | ✅ | Diagnosis Loop (lines 24–85) is procedural with 6 phase sections (~50 lines total); Dot graph (lines 141–163) is embedded but relevant to flow; no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ✅ | Phase 4 (INSTRUMENT) lines 61–66 explicitly says "never merge debug logs" + Phase 5 says "Remove all instrumentation" (fallback for temporary logging); Phase 6 requires regression test before committing fix (prevents silent failures) |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` or offline eval fixture directory in SKILL.md |

**Total**: 4.5/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗
- **Location**: Lines 20–85
- **Gap**: 
  - Lines 88–98 describe error types to triage but do NOT state what input triggers this skill (is it a failing test? a build error? a runtime panic?)
  - Line 34 says "If you cannot reproduce it consistently, STOP" but does not define BLOCKED vs. NEEDS_CONTEXT behavior
  - Lines 114–117 (Red Flags) mention "3 failed fix attempts" escalation but no input validation for whether a root cause is actually identifiable before entering the loop
- **Impact**: Unclear when to invoke skill vs. when to invoke other skills; Implementer may spin in INSTRUMENT phase without recognizing unsolvable scenarios

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory for drift monitoring; no offline case examples (e.g., test failures, build errors, stack traces) to validate skill behavior across Claude versions
- **Impact**: Cannot verify debug diagnosis methodology remains sound as model capabilities evolve; skill drift undetectable

## Recommended Next Step

**Action**: Add input specification + fixture reference
1. Add to `<what-to-do>` (before Step 1): explicit input block listing failure signatures this skill handles (test RED, build error, runtime exception, etc.)
2. Add to "Stop" condition (line 34): explicit NEEDS_CONTEXT behavior with required information
3. Add `<supporting-info>`: "Drift monitoring via `tests/fixtures/s4-local-debug/` (example cases: build errors, test failures, race conditions, stack traces)"

