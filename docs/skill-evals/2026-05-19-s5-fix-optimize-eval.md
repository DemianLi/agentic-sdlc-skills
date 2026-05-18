# Skill Eval — s5-fix-optimize — 2026-05-19

**File**: `skills/s5-fix-optimize/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 46–50: `<supporting-info>` names upstream `/s5-pr-review` and downstream "Stage 6 (QA Engineer)", explains role as "finisher" polishing code to production-readiness |
| 2 | 雙向阻斷 | ✅ | Line 7–19: `<HARD-GATE>` with "Do NOT hand off to Stage 6 if any test is failing"; Red Flags table (line 31–37) provides 3 concrete counter-examples (manual vs. machine verification, lack of regression testing, ignoring WARNINGs) |
| 3 | 輸入清洗 | ✅ | Inputs explicitly listed (line 24): PR review report from `/s5-pr-review`. Failure scenarios defined: line 44 completion states include "NEEDS_CONTEXT — PR review report is missing or incomplete." Handling specified for missing input. |
| 4 | 漸進披露 | ✅ | All inline blocks well under 50 lines. Red Flags table: 7 lines. Workflow steps (lines 22–29): prose, <20 lines. Completion Report (line 39–44): 6 lines. No large templates embedded. |
| 5 | 優雅降級 | ⚠️ | External dependencies: PR review report read, test suite runs (write/execute). Line 25 says "Load PR review report" with no fallback if missing. Completion state "NEEDS_CONTEXT" (line 44) exists but no explicit BLOCKED label in workflow step. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` directory referenced anywhere in SKILL.md. No fixture path, test samples, or eval cases mentioned. Criterion 6 FAIL. |

**Total**: 4/6 PASS — DRAFT

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Line 24–25 (Step 1 in `<what-to-do>`)
- **Gap**: "Load the PR review report from `/s5-pr-review`" (line 24) assumes report exists. No fallback path if report is missing. Completion state "NEEDS_CONTEXT" (line 44) exists but workflow has no early BLOCKED check.
- **Impact**: If PR review report is missing, skill proceeds with incomplete data, producing an invalid fix summary. Should BLOCKED immediately if report cannot be loaded.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory. No fixture samples, test cases, or regression test templates mentioned.
- **Impact**: Cannot verify skill behavior consistency. Skill's fixing strategy changes silently with model updates; no offline eval set exists to catch regressions.

## Recommended Next Step

Create `tests/fixtures/` directory with sample PR review reports and test suites (e.g., `tests/fixtures/2026-05-19-pr-reports/`) for drift monitoring. Add explicit BLOCKED check at Step 1 if PR review report is not found or is incomplete.
